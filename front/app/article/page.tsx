// import { Container } from "@/components/shared/container";
// import { ElementCard } from "@/components/shared/element-card";
// import { Header } from "@/components/shared/header";
// import { Setting } from "@/components/shared/setting";
import React from "react";

interface Props {
  className?: string;
}

export default function Article({}: Props) {
  return (
    <>
      {/* <div className="w-full">
        <Header isAuth={false} />
        <Setting />
      </div>
      <Container className="grid grid-cols-2 gap-10 mt-20">
        {[...new Array(10)].map((_, i) => (
          <ElementCard key={i} />
        ))}
      </Container> */}
    </>
  );
}
