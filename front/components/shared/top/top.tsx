import React from "react";
import { cn } from "@/lib/utils";
import BG from "@/public/img/bg.jpg";
import Image from "next/image";
import classes from "./index.module.scss";

import { TopOfferPopup } from "../top-offer-popup";

interface Props {
  className?: string;
  ref?: React.MutableRefObject<null>;
}

export const Top = ({ className, ref }: Props) => {
  return (
    <div ref={ref} className={cn("group relative z-[1] h-min", className)}>
      <Image src={BG} alt="background" className=" top-0 left-0 w-full" />
      <div className={cn(classes.bg)}></div>
      <TopOfferPopup />
    </div>
  );
};
