import { cn } from "@/lib/utils";
import React from "react";

interface Props {
  className?: string;
}

export const LoginForm = ({ className }: Props) => {
  return (
    <div
      className={cn(
        "p-10 top-1/2 -translate-y-1/2 backdrop-blur-2xl rounded-2xl absolute right-1/4 z-10",
        className
      )}
    >
      <form action="" className="flex flex-col w-[420px]">
        <div className="flex flex-col gap-4 font-semibold text-xl">
          <input
            type="text"
            placeholder="Логин"
            className="rounded-xl outline-none bg-white pl-4 py-3   "
          />
          <input type="password" placeholder="Пароль" />
        </div>
      </form>
    </div>
  );
};
