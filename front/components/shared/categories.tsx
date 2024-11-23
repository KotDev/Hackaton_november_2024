"use client";

import { useCategory } from "@/store/store";
import { cn } from "@/lib/utils";
import Link from "next/link";
import React from "react";

interface Props {
  className?: string;
}

const cats = [
  {
    id: 0,
    name: "Все",
  },
  {
    id: 1,
    name: "Гранты",
  },
  {
    id: 2,
    name: "Субсидии",
  },
  {
    id: 3,
    name: "Ставка по кредиту",
  },
  {
    id: 4,
    name: "Скидки",
  },
];

export const Categories = ({ className }: Props) => {
  const activeCategory = useCategory((state) => state.activeCategory);

  return (
    <div
      className={cn("inline-flex bg-gray-100 p-1 rounded-2xl z-10", className)}
    >
      {cats.map(({ name, id }) => (
        <Link
          href={`/#${name}`}
          className={cn(
            "flex items-center font-bold h-11 px-6 z-20 group relative justify-center overflow-hidden hover:bg-gray-300 rounded-2xl transition duration-200",
            id === activeCategory && "text-secondary"
          )}
          key={id}
        >
          <div
            className={cn(
              "w-full bg-black absolute h-full z-10 transition duration-500 -translate-x-full rounded-r-2xl opacity-0",
              id == activeCategory &&
                "transition duration-500 translate-x-0 rounded-2xl visible opacity-100",
              id == activeCategory - 1 &&
                "translate-x-full rounded-l-2xl visible"
            )}
          ></div>
          <button className="z-[11]">{name}</button>
        </Link>
      ))}
    </div>
  );
};
