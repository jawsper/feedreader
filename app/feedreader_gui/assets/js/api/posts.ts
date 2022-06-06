import { debounce } from "lodash";
import { get } from "svelte/store";

import { api_request } from "./base";
import {
  posts as posts_store,
  outline as outline_store,
  outlines as outlines_store,
  toasts as toasts_store,
  unreadPosts,
} from "../stores";
import type {
  IGetPostsResult,
  IGetUnreadResult,
  IPostActionResult,
} from "./types";
import type { IOutline } from "../types";

const g_limit = 10;

export const load_posts = debounce(
  (a_outline_id: number) => {
    if (!a_outline_id) {
      posts_store.set([]);
      return;
    }

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    api_request(
      "get_posts",
      { limit: g_limit, outline: a_outline_id },
      (data: IGetPostsResult) => {
        if (data.success) {
          const { posts, success, ...rest } = data;
          outline_store.set({
            id: a_outline_id,
            ...rest,
          });
          get_unread_counts();

          requestAnimationFrame(() =>
            window.scrollTo({
              top: 0,
              left: 0,
              // @ts-ignore
              behavior: "instant",
            })
          );

          posts_store.current_id.set(null);
          if (data.posts.length > 0) {
            posts_store.set(posts);
            posts_store.no_more_posts.set(false);
          } else {
            posts_store.set([]);
            posts_store.no_more_posts.set(true);
          }
          posts_store.loading.set(false);
        }
      }
    );
  },
  500,
  { leading: true }
);

export const load_more_posts = debounce(
  () => {
    const outline = get(outline_store);
    if (!outline) return;
    const { id: outline_id } = outline;

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    let skip = get(unreadPosts);

    api_request(
      "get_posts",
      { outline: outline_id, skip, limit: g_limit },
      (data: IGetPostsResult) => {
        if (data.success) {
          if (data.posts.length > 0) {
            posts_store.append(data.posts);
            posts_store.no_more_posts.set(false);
          } else {
            posts_store.no_more_posts.set(true);
          }
          posts_store.loading.set(false);
        }
      }
    );
  },
  500,
  { leading: true }
);

export const get_unread_counts = debounce(
  () => {
    const outline = get(outline_store);
    if (!outline) return;
    const { id: outline_id } = outline;
    api_request("get_unread", { outline_id }, (data: IGetUnreadResult) => {
      document.title =
        data.total > 0 ? `Feedreader (${data.total})` : "Feedreader";
      if (!data.counts) return;

      const update_outline = (outline: IOutline) => {
        if (data.counts[`${outline.id}`] !== undefined) {
          outline.unread_count = data.counts[`${outline.id}`];
        }
        if (outline.children) {
          for (const child of outline.children) {
            update_outline(child);
          }
        }
      };

      outlines_store.update((outlines) => {
        for (const outline of outlines) {
          update_outline(outline);
        }
        return outlines;
      });

      outline_store.update(($outline) => {
        if ($outline?.id === outline_id) {
          return {
            ...$outline,
            unread_count: data.counts[`${outline_id}`],
          };
        }
        return $outline;
      });
    });
  },
  500,
  { trailing: true }
);

export const set_post_attr_state = (
  post_id: number,
  attr: "read" | "starred",
  state: boolean
) => {
  api_request(
    "post_action",
    { post: post_id, action: attr, state: state },
    (data: IPostActionResult) => {
      toasts_store.push(data, { context: `${post_id}` });
      if (data.success) get_unread_counts();
    }
  );
};
