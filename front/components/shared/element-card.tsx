import React from "react";
import { Button } from "./button";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface ICategory {
  tag_id: number;
  name: string;
}

interface ICard {
  title?: string;
  description?: string;
  date?: string;
  news_id: number;
  tags?: ICategory[];
  link?: URL;
}

interface Props extends ICard {
  className?: string;
}

export const ElementCard = ({
  className,
  title,
  description,
  date,
  news_id,
  tags,
  link,
}: Props) => {
  const [isActive, setIsActive] = React.useState(false);

  return (
    <div
      className={cn(
        "border-y-2 py-8 hover:scale-[1.02] hover:shadow-sm transition duration-300 ",
        className
      )}
    >
      <div className="flex flex-col gap-4">
        <div className="max-w-[90%]">
          {tags?.map((e) => (
            <p
              key={e.tag_id}
              className="lowercase font-medium text-primary text-sm border-primary border w-max px-2 py-[2px] rounded-md"
            >
              {e.name}
            </p>
          ))}
        </div>
        <Link
          href={link || `#${news_id}`}
          className="text-white font-semibold text-2xl"
        >
          {title}
        </Link>
        <p className="text-gray-100 ">{date}</p>
      </div>
      {isActive && <div className="">{description}</div>}
      <Button
        type={"button"}
        variant={"default"}
        onClick={() => setIsActive(!isActive)}
      >
        Подробнее
      </Button>
    </div>
  );
};
