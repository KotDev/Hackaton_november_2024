"use client";

import { useCategory } from "@/store/store";
import { cn } from "@/lib/utils";
import React from "react";
import { api } from "@/Api/Auth/route";
import { useRouter, useSearchParams } from "next/navigation";
import { useSet } from "react-use";
import qs from "qs";

interface Props {
  className?: string;
}

interface ICategory {
  tag_id: number;
  name: string;
}
interface QueryFilters {
  category: string;
}

export const Categories = ({ className }: Props) => {
  const { activeCategory, setActiveCategory } = useCategory((state) => state);
  const [isLoad, setIsLoad] = React.useState<boolean>(false);

  const [category, setCategory] = React.useState<ICategory[]>([]);

  const router = useRouter();

  const searchParams = useSearchParams() as unknown as Map<
    keyof QueryFilters,
    string
  >;

  const [selected, { toggle: toggle }] = useSet<string>(
    new Set(
      searchParams.has("category")
        ? searchParams.get("category")?.split(",")
        : []
    )
  );

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

  React.useEffect(() => {
    if (selected.size === 0) return;

    const filters = {
      category: Array.from(selected),
    };

    setActiveCategory(Array.from(selected));

    const query = qs.stringify(filters, {
      arrayFormat: "comma",
    });

    router.push(`?${query}`, { scroll: false });
  }, [selected, router]);

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
              activeCategory.includes(String(e.tag_id)) && "text-secondary"
            )}
            key={e.tag_id}
          >
            <button className="z-[11]" onClick={() => toggle(String(e.tag_id))}>
              {e.name}
            </button>
          </div>
        ))}
    </div>
  );
};
