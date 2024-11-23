import React from "react";
import { Button } from "./button";
import { cn } from "@/lib/utils";

interface Props {
  className?: string;
}

export const ElementCard = ({ className }: Props) => {
  return (
    <div
      className={cn(
        "border-y-2 py-8 hover:scale-[1.02] hover:shadow-sm transition duration-300 ",
        className
      )}
    >
      <div className="flex flex-col gap-4">
        <div className="">
          <p className="lowercase font-medium text-primary text-sm border-primary border w-max px-2 py-[2px] rounded-md">
            гранты
          </p>
        </div>
        <h3 className="text-white font-semibold text-2xl">
          Валерий Выжутович - о кредитовании среднего и малого бизнеса
        </h3>
        <p className="text-gray-100 ">22.11.2024</p>
      </div>
      <Button type={"button"} variant={"default"}>
        Подробнее
      </Button>
    </div>
  );
};
