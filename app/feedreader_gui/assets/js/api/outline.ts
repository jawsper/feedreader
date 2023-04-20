import { outlines, outlines_loading } from "../stores";
import { load_posts } from "./posts";

import { api } from "./base";

export const set_outline_param = async (
  outline_id: number,
  key: "folder_opened" | "show_only_new" | "sort_order_asc",
  value: boolean,
  no_load?: boolean | null
) => {
  if (!outline_id) return;

  try {

    const result = await api.partialUpdateSingleOutline({
      id: `${outline_id}`,
      singleOutline: {
        [key]: value,
      }
    });
    if (result) {
      if (!no_load) load_posts(outline_id);
    }
  } finally {
  }
};

export const mark_all_as_read = async (outline_id: number) => {
  console.warn("mark all as read not implemented yet")
  // if (!outline_id) return;
  // try {
  //   const response = await api_request<any>("outline_mark_read", {
  //     outline: outline_id,
  //   });
  //   if (!response.error) load_posts(outline_id);
  // } finally {
  // }
};

export const load_navigation = async () => {
  outlines_loading.set(true);
  try {
    const data = await api.listOutlines()
    outlines.set(data)
  } finally {
    outlines_loading.set(false);
  }
};
