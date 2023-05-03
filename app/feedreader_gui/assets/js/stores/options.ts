import { writable } from "svelte/store";

import type { Config } from "../api/gen";

const config = JSON.parse(document.getElementById("config").textContent) as Config;

type OptionType = "boolean";

interface Option<T extends OptionType> {
  title: string;
  type: T;
  default: any;
  value: any;
}

export interface Options {
  show_only_unread: Option<"boolean">;
  show_nsfw_feeds: Option<"boolean">;
}

const optionsDefault: Options = {
  show_only_unread: {
    title: "Show only unread posts",
    type: "boolean",
    default: true,
    value: undefined,
  },
  show_nsfw_feeds: {
    title: "Show NSFW feeds",
    type: "boolean",
    default: false,
    value: undefined,
  },
};

for(const [k, v] of Object.entries(config)) {
  optionsDefault[k].value = v
}

const createOptions = () => {
  const { subscribe, set, update } = writable<Options>(optionsDefault);

  return {
    subscribe,
    set: (name: keyof Options, value: any) => {
      update((values) => ({
        ...values,
        [name]: {
          ...values[name],
          value,
        },
      }));
    },
  };
};

export const options = createOptions();
