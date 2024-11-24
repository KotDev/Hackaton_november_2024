import { api } from "@/Api/Auth/route";
import { cn } from "@/lib/utils";
import React from "react";

interface Props {
  className?: string;
}

interface ITokens {
  access_token: string;
  refresh_token: string;
  token_type: "Bearer";
}

export const ProfileCard = ({ className }: Props) => {
  //const { ProfileInfo } = useProfileInfo((state) => state);
  const [tokens, setTokens] = React.useState<ITokens>({
    refresh_token: "",
    access_token: "",
    token_type: "Bearer",
  });

  React.useEffect(() => {
    const data = localStorage.getItem("tokens");
    if (data) {
      setTokens(JSON.parse(data));
    }
  }, []);

  React.useEffect(() => {
    if (tokens.access_token === "") {
      return;
    }
    api
      .post("/profile/new_profile", {
        headers: {
          Authorization: `Bearer ${tokens.access_token}`,
          "x-refresh-token": tokens.refresh_token,
        },
      })
      .then((response) => console.log(response))
      .catch((err) => console.error(err));
  }, [tokens]);

  return (
    <div className={cn("", className)}>
      <div className="">
        <h4 className="text-3xl uppercase font-bold text-primary mb-10">
          Ваши данные:
        </h4>
        <div className="">
          <p></p>
        </div>
      </div>
      <div className=""></div>
    </div>
  );
};
