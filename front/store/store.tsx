import { create } from "zustand";

interface IUseCategory {
  activeCategory: number;
  setActiveCategory: (value: number) => void;
}

export const useCategory = create<IUseCategory>()((set) => ({
  activeCategory: 0,
  setActiveCategory: (value) => set(() => ({ activeCategory: value })),
}));

interface IUseAuthForm {
  isActive: boolean;
  activeForm: "signin" | "login";
  setIsActive: (value: boolean) => void;
  setActiveForm: (value: "signin" | "login") => void;
}

export const useAuthForm = create<IUseAuthForm>()((set) => ({
  isActive: false,
  activeForm: "signin",
  setIsActive: (value) => set(() => ({ isActive: value })),
  setActiveForm: (value) => set(() => ({ activeForm: value })),
}));