"use client";

import { cn } from "@/lib/utils";
import { Eye, Mail } from "lucide-react";
import React from "react";

interface Props {
  className?: string;
  type: string;
  children?: React.ReactElement | string;
  placeholder?: string;
  required?: boolean;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export const Input = ({
  className,
  children,
  placeholder,
  value,
  onChange,
  required = false,
  type = "text",
}: Props) => {
  const [isVisible, setIsVisible] = React.useState<boolean>(false);

  return (
    <div
      className={cn(
        "py-3 px-6 text-black font-semibold rounded-2xl bg-secondary flex items-center gap-6 hover:scale-[1.02]",
        className
      )}
    >
      {type === "email" && <Mail size={20} />}
      {type === "password" && (
        <Eye
          size={20}
          className="cursor-pointer"
          onClick={() => setIsVisible(!isVisible)}
        />
      )}
      <input
        onChange={onChange}
        value={value}
        required={required}
        className="outline-none bg-secondary"
        placeholder={placeholder}
        type={!isVisible ? type : "text"}
      >
        {children}
      </input>
    </div>
  );
};
