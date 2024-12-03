import openai

# Установите свой API-ключ OpenAI
openai.api_key = ""

def summarize_text(input_text: str) -> str:
    """
    Функция для генерации резюме текста с использованием OpenAI GPT-4.

    :param input_text: Текст, который требуется суммировать.
    :return: Краткое резюме текста.
    """
    if not input_text.strip():
        return "Ошибка: Текст для резюмирования пуст."

    try:
        # Промпт для резюмирования
        system_prompt = "Ты помощник, который кратко резюмирует предоставленные тексты."
        user_prompt = f"Сделай краткое резюме следующего текста:\n{input_text}"

        # Запрос к GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
        )

        # Извлечение резюме из ответа
        summary = response["choices"][0]["message"]["content"]
        return summary.strip()
    except Exception as e:
        return f"Ошибка при вызове API: {str(e)}"