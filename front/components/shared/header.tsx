import React from "react";
import { Container } from "./container";
import { cn } from "@/lib/utils";
import Image from "next/image";
import LOGO from "@/public/img/svg/logo.svg";
import { Button } from "./button";

interface Props {
  className?: string;
}

export const Header = ({ className }: Props) => {
  return (
    <header className={cn("bg-black/80 py-6 z-30 w-full", className)}>
      <Container className="flex justify-between">
        <div className="flex items-center gap-4">
          <Image src={LOGO} alt="LOGO" width={60} height={60} />
          <h2 className="text-2xl font-semibold uppercase text-secondary">
            льгота.ру
          </h2>
        </div>
        <div className="flex items-center gap-6">
          <Button type="button" className="w-[200px]" variant={"secondary"}>
            Регистрация
          </Button>
          <Button type="button" className="w-[200px]" variant={"secondary"}>
            Вход
          </Button>
        </div>
      </Container>
    </header>
  );
};
