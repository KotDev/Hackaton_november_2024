"use client";
import { cn } from "@/lib/utils";
import { useSorting } from "@/store/store";
import { ArrowDown, ArrowUp } from "lucide-react";
import React from "react";

interface Props {
  className?: string;
}

export const Sorting = ({ className }: Props) => {
  const [sortUp, setSortUp] = React.useState<boolean>(true);
  const { setUp } = useSorting((state) => state);

  React.useEffect(() => {
    setUp(sortUp);
  }, [sortUp]);

  return (
    <div
      onClick={() => setSortUp(!sortUp)}
      className={cn(
        "inline-flex items-center gap-1 bg-gray-50 px-5 h-[52px] rounded-2xl transition duration-200 cursor-pointer",
        !sortUp && "bg-black text-secondary outline-2 outline",
        className
      )}
    >
      {sortUp ? <ArrowDown size={18} /> : <ArrowUp size={18} />}
      <b>Сортировка по </b>
      <b
        className={cn(
          "text-secondary bg-black px-4 py-1 rounded-lg transition duration-200",
          !sortUp && "text-black bg-gray-50 "
        )}
      >
        дате
      </b>
    </div>
  );
};
