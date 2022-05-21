import { api_request } from "./base";
import { load_posts } from "./posts";

export const set_outline_param = (outline_id, key, value, no_load) => {
  if (!outline_id) return;
  let request = { outline: outline_id, action: key };
  if (value) request["value"] = value;

  api_request("outline_set", request, (response) => {
    if (response.success) {
      if (!no_load) load_posts(outline_id);
    }
  });
};

export const mark_all_as_read = (outline_id) => {
  if (!outline_id) return;
  api_request("outline_mark_read", { outline: outline_id }, (response) => {
    if (!response.error) load_posts(outline_id);
  });
};
