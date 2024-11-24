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
import { api } from "@/Api/Auth/route";

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

// interface QueryFilters {
//   tags: string;
// }

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

  const [category, setCategory] = React.useState<ICategory[]>([]);

  React.useEffect(() => {
    api
      .get("/news/tags")
      .then((response) => {
        setCategory(response.data);
      })
      .catch((err) => console.error(err));
  }, []);

  const [articleElements, setArticleData] = React.useState<ICard[]>([]);

  React.useEffect(() => {
    api
      .get("/news/all_news")
      .then((response) => {
        setArticleData(response.data);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="">
      <Header
        isAuth={true}
        className={cn(
          "fixed top-0 left-0 opacity-100 transition-opacity duration-200",
          !activeHeader && "opacity-0"
        )}
      />
      <Top ref={interSectionRef} />
      <Setting tags={category} />
      <Container className="grid grid-cols-2 gap-16 mt-[120px]">
        {articleElements.map((e, _) => (
          <ElementCard
            news_id={e.news_id}
            link={e.link}
            date={e.date}
            description={e.description}
            tags={e.tags}
            key={e.news_id}
          />
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
