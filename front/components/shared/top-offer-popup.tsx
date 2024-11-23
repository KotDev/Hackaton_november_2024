"use client";
import React from "react";
import { Button } from "./button";
import { cn } from "@/lib/utils";
import LOGO from "@/public/img/svg/logo-2.svg";
import Image from "next/image";
import { useAuthForm } from "@/store/store";

interface Props {
  className?: string;
}

export const TopOfferPopup = ({ className }: Props) => {
  const { setIsActive } = useAuthForm((state) => state);

  return (
    <div
      className={cn(
        "backdrop-blur-xl rounded-2xl w-[600px] z-10 absolute top-1/2 -translate-y-1/2 right-[10%] flex flex-col items-center gap-10 p-20 hover:backdrop-blur-2xl transition duration-300 shadow-white shadow-sm hover:scale-[1.02]",
        className
      )}
    >
      <div className="flex items-center gap-3">
        <Image src={LOGO} alt="LOGO" />
        <div className="flex flex-col justify-start">
          <h2 className="font-bold text-white text-3xl uppercase">льгота.ру</h2>
          <p className="font-medium text-primary text-sm leading-none max-w-44">
            персональный подбор гос. преимуществ
          </p>
        </div>
      </div>

      <p className="font-medium leading-[1.2] text-3xl text-secondary">
        Попробуйте персональную подборку помощи от государства для вашего дела
      </p>

      <Button
        type={"button"}
        className="w-full"
        variant={"outline"}
        onClick={() => setIsActive(true)}
      >
        Попробовать
      </Button>
    </div>
  );
};
