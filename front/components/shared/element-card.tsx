import React from "react";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface ICategory {
  tag_id: number;
  name: string;
}

interface INews {
  title: string;
  description: string;
  date: string;
  news_id: number;
  link: string;
}

interface ICard {
  news: INews;
  tags: ICategory[];
}

interface Props extends ICard {
  className?: string;
}

export const ElementCard = ({ className, news, tags }: Props) => {
  const [isActive, setIsActive] = React.useState(false);

  return (
    <div
      className={cn(
        "border-y-2 py-8 hover:scale-[1.02] hover:shadow-sm transition duration-300 ",
        className
      )}
    >
      <div className="flex flex-col gap-4 relative group">
        <div className="max-w-[80%] s overflow-x-scroll flex gap-1">
          {tags?.map((e) => (
            <p
              key={e.tag_id + "tag"}
              className="lowercase font-medium text-primary text-sm border-primary border w-max px-2 py-[2px] rounded-md"
            >
              {e.name}
            </p>
          ))}
        </div>
        <a href={news.link} className="text-white font-semibold text-2xl">
          {news.title}
        </a>
        <p className="text-gray-100 ">{news.date}</p>
      </div>
      {isActive && (
        <div className="text-white font-normal text-sm">{news.description}</div>
      )}
      <Link
        onClick={() => setIsActive(!isActive)}
        href={`/#${news.title}`}
        className="text-black bg-white border-white font-medium text-lg px-4 py-2 hover:bg-black hover:text-white transition duration-200"
      >
        Подробнее
      </Link>
    </div>
  );
};
