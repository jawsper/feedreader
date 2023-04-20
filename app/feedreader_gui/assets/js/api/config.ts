import { api } from "./base";
import type { Config } from "./gen";

export const update_config = async (config: Config) => {
  return await api.partialUpdateConfig({
    config,
  });
};
