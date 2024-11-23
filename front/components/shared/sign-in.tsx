"use client";
import { cn } from "@/lib/utils";
import React from "react";
import { Input } from "./input";
import { Button } from "./button";
import { useAuthForm } from "@/store/store";

interface Props {
  className?: string;
}

export const SignInForm = ({ className }: Props) => {
  const { setActiveForm } = useAuthForm((state) => state);
  return (
    <div
      className={cn(
        "absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 py-20 px-14 bg-black shadow-xl shadow-secondary rounded-2xl",
        className
      )}
    >
      <form action="POST" className="flex flex-col items-center">
        <h5 className="text-3xl uppercase font-bold text-primary mb-10">
          РЕгестрация
        </h5>
        <div className="flex flex-col gap-3 mb-10">
          <Input type="email" placeholder="Введите почту" />
          <Input type="password" placeholder="Введите пароль" />
          <Input type="password" placeholder="Введите пароль" />
        </div>
        <Button type="submit" variant={"outline"} className="w-full">
          Зарегестрироваться
        </Button>
        <button
          onClick={() => setActiveForm("login")}
          type="button"
          className="text-secondary font-light text-md hover:underline"
        >
          Уже есть аккаунт
        </button>
      </form>
    </div>
  );
};
