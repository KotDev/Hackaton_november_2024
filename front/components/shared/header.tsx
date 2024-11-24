import React from "react";
import { Container } from "./container";
import { cn } from "@/lib/utils";
import Image from "next/image";
import LOGO from "@/public/img/svg/logo.svg";
import { Button } from "./button";
import { User } from "lucide-react";

interface Props {
  className?: string;
  isAuth: boolean;
}

export const Header = ({ className, isAuth }: Props) => {
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
          {isAuth ? (
            <>
              <Button type="button" className="w-[200px]" variant={"secondary"}>
                Регистрация
              </Button>
              <Button type="button" className="w-[200px]" variant={"secondary"}>
                Вход
              </Button>
            </>
          ) : (
            <>
              <Button
                type="button"
                variant={"secondary"}
                className="p-2 rounded-full group"
              >
                <User size={25} color={"white"} />
              </Button>
            </>
          )}
        </div>
      </Container>
    </header>
  );
};
