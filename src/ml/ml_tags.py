import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import shutil
import sys
import os

MAX_LEN = 256
TRAIN_BATCH_SIZE = 64
VALID_BATCH_SIZE = 64
EPOCHS = 1
LEARNING_RATE = 1e-05
THRESHOLD = 0.5

from transformers import BertTokenizer, BertModel
tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny')

target_list = ['Частный', 'Государственный', 'Муниципальный', 'Смешанный', 'Стартап', 'Малый', 'Средний', 'Крупный','Локальный', 'Региональный', 'Международный','Физ.Лица', 'Юр.Лица', 'UnrelevantText']
another_categories = ['Частный', 'Государственный', 'Муниципальный', 'Смешанный', 'Стартап', 'Малый', 'Средний', 'Крупный','Локальный', 'Региональный', 'Международный','Физ.Лица', 'Юр.Лица', 'UnrelevantText']

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, df, tokenizer, max_len):
        self.tokenizer = tokenizer
        self.df = df
        self.title = df['CONTEXT']
        self.targets = self.df[target_list].values
        self.max_len = max_len

    def __len__(self):
        return len(self.title)

    def __getitem__(self, index):
        title = str(self.title[index])
        title = " ".join(title.split())

        inputs = self.tokenizer.encode_plus(
            title,  # Combine header and body as needed
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        return {
            'input_ids': inputs['input_ids'].flatten(),
            'attention_mask': inputs['attention_mask'].flatten(),
            'token_type_ids': inputs["token_type_ids"].flatten(),
            'targets': torch.FloatTensor(self.targets[index])
        }

class TokenizedArticle(CustomDataset):
    def __init__(self, tokenizer, header, body):
        self.tokenizer = tokenizer
        self.header = header
        self.body = body
    def __len__(self):
        super().__len__(self.title)
    def __getitem__(self, index):
        super().__getitem__(index)

        inputs = self.tokenizer.encode_plus(
          None,
          add_special_tokens=True,
          max_length=self.max_len,
          padding='max_length',
          return_token_type_ids=True,
          truncation=True,
          return_attention_mask=True,
          return_tensors='pt'
        )

        return {
            'input_ids': inputs['input_ids'].flatten(),
            'attention_mask': inputs['attention_mask'].flatten(),
            'token_type_ids': inputs["token_type_ids"].flatten(),
        }

class BERTClass(torch.nn.Module):
    def __init__(self, isTraining, tokenizer, threshold):
        super(BERTClass, self).__init__()
        self.bert_model = BertModel.from_pretrained('cointegrated/rubert-tiny', return_dict=True)
        self.dropout = torch.nn.Dropout(0.4)
        self.isTraining = isTraining
        self.choosentokenizer = tokenizer
        self.threshold = threshold

        """
        # Линейные слои для каждой группы взаимоисключающих категорий
        self.fc_exclusive1 = torch.nn.Linear(312, 4)  # "Стартап", "Малый", "Средний", "Крупный"
        self.fc_exclusive2 = torch.nn.Linear(312, 4)  # "Частный", "Государственный"
        self.fc_exclusive3 = torch.nn.Linear(312, 2)  # "Физ.Лица", "Юр.Лица"
        self.fc_exclusive4 = torch.nn.Linear(312, 3)  # "Локальный", "Региональный", "Международный"
        """

        # Линейный слой для оставшихся независимых категорий
        self.fc_others = torch.nn.Linear(312, 14)  # "UnrelevantText"

        # Линейный слой для определения релевантности текста
        self.fc_relevance = torch.nn.Linear(312, 2)  # "Релевантный" или "Нерелевантный"

    def forward(self, input_ids, attn_mask, token_type_ids):
        # Выход BERT модели
        output = self.bert_model(
            input_ids,
            attention_mask=attn_mask,
            token_type_ids=token_type_ids
        )
        pooled_output = self.dropout(output.pooler_output)

        """
        # Взаимоисключающие категории
        output_exclusive1 = torch.softmax(self.fc_exclusive1(pooled_output), dim=1)
        output_exclusive2 = torch.softmax(self.fc_exclusive2(pooled_output), dim=1)
        output_exclusive3 = torch.softmax(self.fc_exclusive3(pooled_output), dim=1)
        output_exclusive4 = torch.softmax(self.fc_exclusive4(pooled_output), dim=1)
        """

        # Применение порога 0.5 к вероятностям
        """
        if not self.isTraining:
          output_exclusive1 = torch.where(output_exclusive1.max(dim=1, keepdim=True).values > self.threshold, output_exclusive1, torch.zeros_like(output_exclusive1))
          output_exclusive2 = torch.where(output_exclusive2.max(dim=1, keepdim=True).values > self.threshold, output_exclusive2, torch.zeros_like(output_exclusive2))
          output_exclusive3 = torch.where(output_exclusive3.max(dim=1, keepdim=True).values > self.threshold, output_exclusive3, torch.zeros_like(output_exclusive3))
          output_exclusive4 = torch.where(output_exclusive4.max(dim=1, keepdim=True).values > self.threshold, output_exclusive4, torch.zeros_like(output_exclusive4))
        """

        # Остальные категории
        output_others = torch.sigmoid(self.fc_others(pooled_output))

        # Релевантность текста
        relevance_logits = self.fc_relevance(pooled_output)  # [batch_size, 2]
        relevance_output = torch.softmax(relevance_logits, dim=1)  # Вероятности релевантности

        # Конкатенация всех предсказаний в один тензор
        final_output = torch.cat([
            #output_exclusive1,  # 4 logits
            #output_exclusive2,  # 4 logits
            #output_exclusive3,  # 2 logits
            #output_exclusive4,  # 3 logits
            output_others       # 1 logit
        ], dim=1)  # Объединяем по последней размерности

        # Бинарный выход: 1, если текст релевантный, иначе 0
        binary_output = torch.argmax(relevance_output, dim=1).float()  # [batch_size]

        return {
            "final_output": final_output,    # Все предсказания
            "binary_output": binary_output,  # Бинарное решение
            "relevance_output": relevance_output,  # Вероятности релевантности
            #"ou1": output_exclusive1,
            #"ou2": output_exclusive2,
            #"ou3": output_exclusive3,
            #"ou4": output_exclusive4,
            "oo": output_others
        }
    def save_weights(self, file_path):
        """
        Сохраняет веса модели в текстовый файл.
        """
        with open(file_path, 'w') as f:
            for layer_name, weight_tensor in self.state_dict().items():
                f.write(f"Layer: {layer_name}\n")
                f.write(f"Shape: {list(weight_tensor.shape)}\n")
                f.write(f"Weights: {weight_tensor.numpy().tolist()}\n")
                f.write("\n")  # Разделитель между слоями
        print(f"Weights saved to {file_path}")

    def load_weights(self, file_path):
        """
        Загружает веса модели из текстового файла.
        """
        import ast  # Для преобразования строки в Python-объект
        state_dict = self.state_dict()
        with open(file_path, 'r') as f:
            lines = f.readlines()

    def save_weights_in_parts(self, folder_path):
        """
        Сохраняет веса модели по частям
        """
        os.makedirs(folder_path, exist_ok=True)

        state_dict = self.state_dict()
        # Сохраняем каждый ключ отдельно
        for key in state_dict:
            part_path = os.path.join(folder_path, f"{key}.pt")
            torch.save({key: state_dict[key]}, part_path)
            print(f"Сохранена часть {key} в файл {part_path}")

    def load_weights_in_parts(self, folder_path):
      """
      Загружает веса модели из всех файлов в указанной папке
      """
      """
      state_dict = {}

      # Перебираем файлы в указанной директории
      for part_file in os.listdir(folder_path):
          part_path = os.path.join(folder_path, part_file)

          # Проверяем, что это файл и он заканчивается на .pt
          if os.path.isfile(part_path) and part_file.endswith(".pt"):
              part = torch.load(part_path)
              state_dict.update(part)
              print(f"Загружена часть из файла {part_path}")
          else:
              print(f"Пропущен файл {part_path}, так как это не .pt файл или это директория.")

      # Загружаем объединенное состояние в модель
      model.load_state_dict(state_dict)
      print("Все части объединены и загружены в модель."
      """
      # Проверяем, что указанная папка существует
      if not os.path.isdir(folder_path):
          raise ValueError(f"Указанный путь {folder_path} не является директорией.")

      # Получаем список файлов .pt
      weight_files = [
          os.path.join(folder_path, file)
          for file in os.listdir(folder_path)
          if os.path.isfile(os.path.join(folder_path, file)) and file.endswith(".pt")
      ]

      if not weight_files:
          raise ValueError(f"В директории {folder_path} не найдено файлов с расширением .pt.")

      # Загружаем веса из каждого файла
      for file_path in weight_files:
          try:
              print(f"Загружается файл весов: {file_path}")
              weights = torch.load(file_path)
              self.load_state_dict(weights, strict=False)  # strict=False, чтобы избежать ошибок несовпадения
              print(f"Файл {file_path} успешно загружен.")
          except Exception as e:
              print(f"Ошибка при загрузке файла {file_path}: {e}")

      print("Все файлы в папке успешно обработаны.")

    def validate_article(self, header, body):
        if not isinstance(header, str) or not isinstance(body, str):
            raise ValueError(f"Invalid input: header='{header}', body='{body}'. Both must be strings.")
        tokenized_article = self.choosentokenizer(
            header, body, padding='max_length', truncation=True, return_tensors='pt'
        )
        results = self.forward(
            tokenized_article['input_ids'],
            tokenized_article['attention_mask'],
            tokenized_article['token_type_ids']
        )
        return results

    def analyze(self, header, body):
        if not header:
            header = "Default Header"  # Replace with a meaningful default or handle the case explicitly
        if not body:
            body = "Default Body"  # Replace with a meaningful default or handle the case explicitly
        resultsOfValidation = self.validate_article(header, body)
        if resultsOfValidation["binary_output"] == 0:
            return "Нерелевантный"
        else:
            tags = []
            bool_mask = resultsOfValidation["oo"] > 0.5

            indices = torch.nonzero(bool_mask)

        # Преобразуем индексы в одномерный список
            tags = [another_categories[idx[1].item()] for idx in indices if idx[1].item() != 13]
        #print(indices)
        """
        # Используем torch.argmax для нахождения индекса максимального значения
        if torch.sum(resultsOfValidation["ou1"]) > 0:
            max_idx = torch.argmax(resultsOfValidation["ou1"]).item()
            tags.append(exclusive_categories1[max_idx])

        if torch.sum(resultsOfValidation["ou2"]) > 0:
            max_idx = torch.argmax(resultsOfValidation["ou2"]).item()
            tags.append(exclusive_categories2[max_idx])

        if torch.sum(resultsOfValidation["ou3"]) > 0:
            max_idx = torch.argmax(resultsOfValidation["ou3"]).item()
            tags.append(exclusive_categories3[max_idx])

        if torch.sum(resultsOfValidation["ou4"]) > 0:
            max_idx = torch.argmax(resultsOfValidation["ou4"]).item()
            tags.append(exclusive_categories4[max_idx])
        """
        return tags


model = BERTClass(False, tokenizer, THRESHOLD)