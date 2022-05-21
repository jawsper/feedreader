import { debounce } from "lodash";
import jquery from "jquery";
import { get } from "svelte/store";

import { api_request } from "./base";
import {
  posts as posts_store,
  outline as outline_store,
  outlines as outlines_store,
  unreadPosts,
} from "../stores";

const g_limit = 10;

export const load_posts = debounce(
  (a_outline_id) => {
    if (!a_outline_id) return;

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    api_request(
      "get_posts",
      { limit: g_limit, outline: a_outline_id },
      (data) => {
        if (data.success) {
          const { posts, ...rest } = data;
          outline_store.set({
            id: a_outline_id,
            ...rest,
          });
          get_unread_counts();

          jquery("#content").scrollTop(0);
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
    const { id: outline } = get(outline_store);

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    let skip = get(unreadPosts);

    api_request("get_posts", { outline, skip, limit: g_limit }, (data) => {
      if (!data.error) {
        if (data.posts.length > 0) {
          posts_store.append(data.posts);
          posts_store.no_more_posts.set(false);
        } else {
          posts_store.no_more_posts.set(true);
        }
        posts_store.loading.set(false);
      }
    });
  },
  500,
  { leading: true }
);

export const get_unread_counts = debounce(
  () => {
    const { id: outline_id } = get(outline_store);
    api_request("get_unread", { outline_id }, (data) => {
      document.title =
        data.total > 0 ? `Feedreader (${data.total})` : "Feedreader";
      if (!data.counts) return;
      outlines_store.update(($outlines) => {
        for (const outline of $outlines.outlines) {
          if (data.counts[`${outline.id}`] !== undefined) {
            outline.unread_count = data.counts[`${outline.id}`];
          }
        }
        return $outlines;
      });

      outline_store.update(($outline) => {
        if ($outline.id === outline_id) {
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
