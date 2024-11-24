import { cn } from "@/lib/utils";
import React from "react";

interface Props {
  className?: string;
  children?: React.ReactElement | string;
  variant: "outline" | "default" | "secondary";
  onClick?: () => void;
  type: "button" | "reset" | "submit" | undefined;
  onSubmit?: React.FormEventHandler<HTMLButtonElement>;
}

export const Button = ({
  className,
  children,
  variant,
  onClick,
  onSubmit,
  type = "button",
}: Props) => {
  const styleRender = (variant: Props["variant"]) => {
    switch (variant) {
      case "default":
        return "w-min";
      case "outline":
        return "px-6 font-semibold py-3 bg-none border-2 border-primary text-primary hover:bg-primary hover:text-white";
      case "secondary":
        return "px-6 font-semibold py-3 bg-none border-2 border-secondary text-secondary hover:bg-secondary hover:text-black";
    }
  };

  return (
    <button
      onSubmit={onSubmit}
      onClick={onClick}
      type={type}
      className={cn(
        "rounded-2xl transition duration-200 hover:scale-[1.1]",
        styleRender(variant),
        className
      )}
    >
      {children}
    </button>
  );
};
