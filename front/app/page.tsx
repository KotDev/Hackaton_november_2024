"use client";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/shared/container";
import { ElementCard } from "@/components/shared/element-card";
import { Footer } from "@/components/shared/footer";
import { Header } from "@/components/shared/header";
import { Setting } from "@/components/shared/setting";
import { Top } from "@/components/shared/top/top";
import { cn } from "@/lib/utils";
import React from "react";
import { useIntersection } from "react-use";
import { AuthForm } from "@/components/shared/auth";

export default function Home() {
  const interSectionRef = React.useRef(null);
  const intersection = useIntersection(interSectionRef, {
    threshold: 0.4,
  });

  const [activeHeader, setActiveHeader] = React.useState<boolean>(false);

  React.useEffect(() => {
    if (intersection?.isIntersecting) {
      setActiveHeader(false);
    } else setActiveHeader(true);
  }, [intersection?.isIntersecting]);

  return (
    <div className="">
      <Header
        className={cn(
          "fixed top-0 left-0 opacity-100 transition-opacity duration-200",
          !activeHeader && "opacity-0"
        )}
      />
      <Top ref={interSectionRef} />
      <Setting />
      <Container className="grid grid-cols-2 gap-16 mt-[120px]">
        {[...new Array(10)].map((_, i) => (
          <ElementCard key={i} />
        ))}
      </Container>
      <Container className="flex justify-center my-[120px]">
        <Button variant="secondary" className={"dark"}>
          Показать еще
        </Button>
      </Container>
      <Footer />
      <AuthForm />
    </div>
  );
}