import { create } from "zustand";

interface IUseCategory {
  activeCategory: string[];
  setActiveCategory: (value: string[]) => void;
}

export const useCategory = create<IUseCategory>()((set) => ({
  activeCategory: [],
  setActiveCategory: (value) => set(() => ({ activeCategory: value })),
}));

interface IUseAuthForm {
  isActive: boolean;
  activeForm: "signin" | "login" | "profile";
  setIsActive: (value: boolean) => void;
  setActiveForm: (value: "signin" | "login" | "profile") => void;
}

export const useAuthForm = create<IUseAuthForm>()((set) => ({
  isActive: false,
  activeForm: "signin",
  setIsActive: (value) => set(() => ({ isActive: value })),
  setActiveForm: (value) => set(() => ({ activeForm: value })),
}));

interface IUseProfileInfo {
  data: object;
  setProfileInfo: (value: object) => void;
}

export const useProfileInfo = create<IUseProfileInfo>()((set) => ({
  data: {},
  setProfileInfo: (value) => set(() => ({ data: value })),
}));

interface IUseBusinesInfo {
  info: object;
  setInfo: (value: object) => void;
}

export const useBusinesInfo = create<IUseBusinesInfo>((set) => ({
  info: {},
  setInfo: (value) => set(() => ({ info: value })),
}));

interface IUseSorting {
  isUp: boolean;
  setUp: (value: boolean) => void;
}

export const useSorting = create<IUseSorting>((set) => ({
  isUp: false,
  setUp: (value) => set(() => ({ isUp: value })),
}));
