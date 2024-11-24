"use client";

import { useCategory } from "@/store/store";
import { cn } from "@/lib/utils";
import React from "react";
import { api } from "@/Api/Auth/route";

interface Props {
  className?: string;
}

interface ICategory {
  tag_id: number;
  name: string;
}

export const Categories = ({ className }: Props) => {
  const activeCategory = useCategory((state) => state.activeCategory);
  const [isLoad, setIsLoad] = React.useState<boolean>(false);

  const [category, setCategory] = React.useState<ICategory[]>([]);

  React.useEffect(() => {
    api
      .get("/news/tags")
      .then((response) => {
        setCategory(response.data.tags_filter);
        setIsLoad(true);
        console.log(response.data.tags_filter);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div
      className={cn(
        "inline-flex bg-gray-100 p-1 rounded-2xl z-10 overflow-x-scroll max-w-[50%]",
        className
      )}
      style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
    >
      {category.length > 0 &&
        category?.map((e) => (
          <div
            className={cn(
              "cursor-pointer",
              "flex items-center font-bold h-11 px-6 z-20 group relative justify-center overflow-hidden hover:bg-gray-300 rounded-2xl transition duration-200 min-w-max",
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
