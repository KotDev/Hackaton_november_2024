import { cn } from "@/lib/utils";
import React, { ReactElement } from "react";

interface Props {
  className?: string;
  children?: ReactElement | ReactElement[];
  ref?: React.MutableRefObject<null>;
}

export const Container = ({ className, children, ref }: Props) => {
  return (
    <div ref={ref} className={cn("mx-auto max-w-[1280px]", className)}>
      {children}
    </div>
  );
};
