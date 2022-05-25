import { writable } from "svelte/store";
import type { IOutline } from "../types";

interface IOutlinesStore {
  loading: boolean;
  outlines: IOutline[];
}

const createOutlines = () => {
  const { subscribe, set, update } = writable<IOutlinesStore>({
    loading: false,
    outlines: [],
  });

  return {
    subscribe,
    set,
    update,
  };
};

export const outlines = createOutlines();
