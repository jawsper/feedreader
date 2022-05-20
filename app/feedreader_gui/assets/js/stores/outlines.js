import { writable } from "svelte/store";

const createOutlines = () => {
  const { subscribe, set, update } = writable([]);

  return {
    subscribe,
    set,
    update,
  };
};

export const outlines = createOutlines();
