"use client";

import { useCategory } from "@/store/store";
import { cn } from "@/lib/utils";
import React from "react";

interface Props {
  className?: string;
  tags: ICategory[];
}

interface ICategory {
  tag_id: number;
  name: string;
}

export const Categories = ({ className, tags }: Props) => {
  const activeCategory = useCategory((state) => state.activeCategory);

  return (
    <div
      className={cn("inline-flex bg-gray-100 p-1 rounded-2xl z-10", className)}
    >
      {tags.map((e) => (
        <div
          className={cn(
            "cursor-pointer",
            "flex items-center font-bold h-11 px-6 z-20 group relative justify-center overflow-hidden hover:bg-gray-300 rounded-2xl transition duration-200",
            activeCategory.includes(e.tag_id) && "text-secondary"
          )}
          key={e.tag_id}
        >
          <button className="z-[11]">{e.name}</button>
        </div>
      ))}
    </div>
  );
};
