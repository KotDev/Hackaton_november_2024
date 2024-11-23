import { cn } from "@/lib/utils";
import React from "react";
import Image from "next/image";
import LOGO from "@/public/img/svg/logo-2.svg";
import TG from "@/public/img/svg/tg.svg";
import VK from "@/public/img/svg/vk.svg";
import TG_2 from "@/public/img/svg/tg-m.svg";
import MAIL from "@/public/img/svg/mail.svg";
import { Container } from "./container";
import Link from "next/link";

interface Props {
  className?: string;
}

export const Footer = ({ className }: Props) => {
  return (
    <footer className={cn("w-full py-10", className)}>
      <Container className="flex items-start justify-between">
        <div className="flex flex-col gap-10">
          <Link href={"/"} className="flex items-center gap-3">
            <Image src={LOGO} alt="LOGO" />
            <div className="flex flex-col justify-start">
              <h2 className="font-bold text-white text-3xl uppercase">
                льгота.ру
              </h2>
              <p className="font-medium text-primary text-sm leading-none max-w-44">
                персональный подбор гос. преимуществ
              </p>
            </div>
          </Link>

          <p className="text-gray-50 font-medium font-lg max-w-[550px]">
            ЛЬГОТА.РУ - сервис предназначенный для помощи предпринимателям в
            поиске мер поддержки крупного и малого бизнеса
          </p>

          <div className="flex items-center gap-5">
            <Link
              href={"vk.com"}
              className={"hover:scale-[1.1] transition duration-200"}
            >
              <Image src={VK} alt="vk profile" />
            </Link>
            <Link href={"tg.com"}>
              <Image
                src={TG}
                alt="telegram profile"
                className="hover:scale-[1.1] transition duration-200"
              />
            </Link>
          </div>
        </div>

        <div className="flex flex-col gap-10 text-gray-50 font-medium font-lg">
          <p>Мы на связи в рабочие дни с 9:00 до 18:00</p>
          <div className="flex flex-col gap-1">
            <Link
              href={"vk.com"}
              className={
                "hover:scale-[1.1] transition duration-200 inline-flex items-center gap-3"
              }
            >
              <Image src={MAIL} width={20} alt="vk profile" />
              service@lgoty.ru
            </Link>
            <Link
              href={"tg.com"}
              className="hover:scale-[1.1] transition duration-200 inline-flex items-center gap-3"
            >
              <Image src={TG_2} width={20} alt="telegram profile" />
              @BiznesLgoty
            </Link>
          </div>
          <div className="flex flex-col gap-1">
            <Link href={"#"} className="font-light hover:underline">
              Политика обработки персональных данных
            </Link>
            <Link href={"#"} className="font-light hover:underline">
              Договор оферта
            </Link>
            <Link href={"#"} className="font-light hover:underline">
              Способы оплаты
            </Link>
          </div>
        </div>
      </Container>
    </footer>
  );
};
