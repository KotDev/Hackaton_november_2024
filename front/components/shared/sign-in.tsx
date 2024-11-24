"use client";
import { cn } from "@/lib/utils";
import React from "react";
import { Input } from "./input";
import { Button } from "./button";
import { useAuthForm } from "@/store/store";
//import { api } from "@/Api/Auth/route";

interface Props {
  className?: string;
}

export const SignInForm = ({ className }: Props) => {
  const { setActiveForm } = useAuthForm((state) => state);
  const [emailValue, setEmailValue] = React.useState<string>("");
  const [passlValue, setPasslValue] = React.useState<string>("");
  const [reqPassValue, setReqPassValue] = React.useState<string>("");

  // const submitHandler = async () => {
  //   const userData = {
  //     email: emailValue,
  //     password: passlValue,
  //     password_verification: reqPassValue,
  //     role: "user",
  //   };
  //   try {
  //     const response = await api.post("/auth/register", userData);
  //     const data = await response.data;
  //     if (typeof window !== "undefined") {
  //       localStorage.setItem("tokens", data);
  //     }
  //     console.log(localStorage);
  //     setProfileInfo(data);
  //   } catch (err) {
  //     console.error(err);
  //   }
  //   setActiveForm("profile");
  // };

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
          <Input
            value={emailValue}
            onChange={({ target }) => setEmailValue(target.value)}
            required={true}
            type="email"
            placeholder="Введите почту"
          />
          <Input
            value={passlValue}
            onChange={({ target }) => setPasslValue(target.value)}
            required={true}
            type="password"
            placeholder="Введите пароль"
          />
          <Input
            value={reqPassValue}
            onChange={({ target }) => setReqPassValue(target.value)}
            required={true}
            type="password"
            placeholder="Введите пароль"
          />
        </div>
        <Button type="button" variant={"outline"} className="w-full">
          Зарегестрироваться
        </Button>
        <button
          onClick={() => setActiveForm("profile")}
          type="button"
          className="text-secondary font-light text-md hover:underline"
        >
          Уже есть аккаунт
        </button>
      </form>
    </div>
  );
};
