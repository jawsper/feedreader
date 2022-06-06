import { writable } from "svelte/store";
import { api_request } from "../api";

const config = JSON.parse(document.getElementById("config").textContent);

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
    load: async () => {
      const keys = Object.keys(optionsDefault);
      try {
        const result = await api_request<any>("get_option", { keys });
        update((options) => {
          for (const [name, option] of Object.entries(options)) {
            if (typeof result.options[name] == "undefined") {
              // key not found
              option.value = option.default;
            } else {
              option.value = result.options[name];
            }
          }
          return { ...options };
        });
      } finally {
      }
    },
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
