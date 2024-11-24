import { cn } from "@/lib/utils";
import React from "react";
import { Categories } from "./categories";
import { Container } from "./container";
import { Title } from "./title";
import { Sorting } from "./sotring";

interface ICategory {
  tag_id: number;
  name: string;
}

interface Props {
  className?: string;
  ref?: React.MutableRefObject<null>;
  tags: ICategory[];
}

export const Setting = ({ className, ref, tags }: Props) => {
  return (
    <Container ref={ref} className={cn("", className)}>
      <Title
        text="Все виды поддержки"
        size="2xl"
        className="text-white font-bold"
      />
      <div className="mt-2 flex justify-between">
        <Categories tags={tags} className="" />
        <Sorting />
      </div>
    </Container>
  );
};
