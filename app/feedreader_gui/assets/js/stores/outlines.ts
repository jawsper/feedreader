import { writable } from "svelte/store";

const createOutlines = () => {
  const { subscribe, set, update } = writable({
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
