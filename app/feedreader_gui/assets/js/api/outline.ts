import { outlines, outlines_loading } from "../stores";
import { api_request } from "./base";
import { load_posts } from "./posts";
import type { IGetAllOutlinesResult } from "./types";

export const set_outline_param = async (
  outline_id: number,
  key: "folder_opened" | "show_only_new" | "sort_order",
  value?: boolean,
  no_load?: boolean | null
) => {
  if (!outline_id) return;
  let request = { outline: outline_id, action: key };
  if (value) request["value"] = value;

  try {
    const response = await api_request<any>("outline_set", request);
    if (response.success) {
      if (!no_load) load_posts(outline_id);
    }
  } finally {
  }
};

export const mark_all_as_read = async (outline_id: number) => {
  if (!outline_id) return;
  try {
    const response = await api_request<any>("outline_mark_read", {
      outline: outline_id,
    });
    if (!response.error) load_posts(outline_id);
  } finally {
  }
};

export const load_navigation = async () => {
  outlines_loading.set(true);
  try {
    const data = await api_request<IGetAllOutlinesResult>(
      "outline_get_all_outlines"
    );
    outlines.set(data.outlines);
  } finally {
    outlines_loading.set(false);
  }
};
