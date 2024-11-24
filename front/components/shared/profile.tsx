//import { api } from "@/Api/Auth/route";
import { cn } from "@/lib/utils";
import React from "react";
import { Dropdown } from "./dropdown";
import { Button } from "./button";
import { useBusinesInfo } from "@/store/store";
import { useRouter } from "next/navigation";

interface Props {
  className?: string;
}

// interface ITokens {
//   access_token: string;
//   refresh_token: string;
//   token_type: "Bearer";
// }

export const ProfileCard = ({ className }: Props) => {
  //const { ProfileInfo } = useProfileInfo((state) => state);
  const { setInfo, info } = useBusinesInfo((state) => state);
  const [form, setForm] = React.useState("");
  const [size, setSize] = React.useState("");
  const [geo, setGeo] = React.useState("");
  const [char, setChar] = React.useState("");
  const route = useRouter();

  React.useEffect(() => {
    console.log(form, size, geo, char);
    if (form && size && geo && char) {
      setInfo({
        form: form,
        size: size,
        geo: geo,
        char: char,
      });
    }
  }, [form, size, geo, char]);
  console.log(info);

  //   const [tokens, setTokens] = React.useState<ITokens>({
  //     refresh_token: "",
  //     access_token: "",
  //     token_type: "Bearer",
  //   });

  //   React.useEffect(() => {
  //     const data = localStorage.getItem("tokens");
  //     if (data) {
  //       setTokens(JSON.parse(data));
  //     }
  //   }, []);

  //   React.useEffect(() => {
  //     if (tokens.access_token === "") {
  //       return;
  //     }
  //     api
  //       .post("/profile/new_profile", {
  //         headers: {
  //           Authorization: `Bearer ${tokens.access_token}`,
  //           "x-refresh-token": tokens.refresh_token,
  //         },
  //       })
  //       .then((response) => console.log(response))
  //       .catch((err) => console.error(err));
  //   }, [tokens]);

  return (
    <div
      className={cn(
        "absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 py-20 px-14 bg-black shadow-xl shadow-secondary rounded-2xl w-[600px]",
        className
      )}
    >
      <div className="flex flex-col gap-10 items-center w-full">
        <h4 className="text-3xl uppercase font-bold text-primary mb-10 text-center">
          Ввведите информацию о бизнесе
        </h4>
        <div className="flex flex-col gap-4 w-full">
          <Dropdown
            setOnChange={setForm}
            items={[
              "Частный бизнес",
              "Государственный бизнес",
              "Муниципальный бизнес",
              "Смешанный",
            ]}
            name="Форма собственности:"
          />
          <Dropdown
            setOnChange={setSize}
            items={["Малый бизнес", "Средний бизнес", "Крупный бизнес"]}
            name="Размер бизнеса:"
          />
          <Dropdown
            setOnChange={setGeo}
            items={["Локальный", "Национальный", "Межрегиональный"]}
            name="По охвату:"
          />
          <Dropdown
            setOnChange={setChar}
            items={["Юридическиое лицо", "Физическое лицо"]}
            name="По характеру организации:"
          />
        </div>
        <Button
          onClick={() => route.push("/article")}
          type={"button"}
          variant={"secondary"}
          className="w-full"
        >
          Сохранить
        </Button>
      </div>
      <div className=""></div>
    </div>
  );
};
