import { cn } from "@/lib/utils";
import { useAuthForm } from "@/store/store";
import React from "react";
import { SignInForm } from "./sign-in";
import { LoginForm } from "./offer-popup";
import { ProfileCard } from "./profile";

interface Props {
  className?: string;
}

export const AuthForm = ({ className }: Props) => {
  const { isActive, activeForm } = useAuthForm((state) => state);
  return (
    <div
      className={cn(
        "fixed top-0 left-0 right-0 bottom-0 backdrop-blur-2xl bg-black/20 z-50",
        !isActive && "hidden",
        className
      )}
    >
      {activeForm === "signin" ? (
        <SignInForm />
      ) : activeForm === "login" ? (
        <LoginForm />
      ) : (
        <ProfileCard />
      )}
    </div>
  );
};
