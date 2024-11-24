import { cn } from "@/lib/utils";
import React from "react";

interface Props {
  className?: string;
  items?: string[];
  name: string;
  setOnChange: (value: string) => void;
}

export const Dropdown = ({ className, items, name, setOnChange }: Props) => {
  const [isActive, setIsActive] = React.useState(false);
  const [choose, setChoose] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (choose !== null) {
      setOnChange(choose);
    }
  }, [choose]);

  return (
    <div
      className={cn("relative cursor-pointer", className)}
      onClick={() => setIsActive(!isActive)}
    >
      <div className="bg-white rounded-xl px-4 py-2 font-medium font-lg">
        {choose || name}
      </div>
      {isActive && (
        <div
          className={cn(
            "w-full bg-gray-200 font-medium font-lg rounded-xl p-4 top-[110%] absolute z-50"
          )}
        >
          {items?.map((element, index) => (
            <div
              className="px-4 py-2 hover:bg-white transition duration-200 rounded-xl hover:scale-[1.005]"
              key={element + index}
              onClick={() => {
                setChoose(element);
                setIsActive(false);
              }}
            >
              {element}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
