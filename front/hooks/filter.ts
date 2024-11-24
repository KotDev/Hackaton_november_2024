import { api } from "@/Api/Auth/route";
import React from "react";
import { useSet } from "react-use";

interface ICategory {
    tag_id:number,
    name:string,
}

interface ReturnProps {
    category: ICategory[],
    isLoading: boolean,
    selectedIds: Set<string>,
    onAddId: (id:string)=>void,
}

export const useFilterCategory = (value?: string[]):ReturnProps=>{
    const [category, setIngredients] = React.useState<ICategory[]>([]);
    const [isLoading, setIsLoading] = React.useState<boolean>(true);

    const [selectedIds, {toggle }] = useSet<string>(new Set(value || []));

    React.useEffect(()=>{
        async function fetchIngredients() {
            try{
                setIsLoading(true);
                const category = await api.get("/news/tags");
                setIngredients(category.data);
            }catch(error) {
                console.log(error);
            }finally{
                setIsLoading(false);
            }
        }
        fetchIngredients();
    }, [])
    return {category, isLoading, onAddId:toggle, selectedIds};
}