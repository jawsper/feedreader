import { debounce } from "lodash";
import jquery from "jquery";
import { get } from "svelte/store";

import { api_request } from "./base";
import {
  posts as posts_store,
  outline as outline_store,
  outlines as outlines_store,
} from "../stores";

const g_limit = 10;

const count_visible_unread_posts = () => {
  // get all unchecked posts and skip those
  // or just all posts
  var count = jquery(
    get(outline_store).show_only_new
      ? "#posts .post .action.read:not(:checked)"
      : "#posts .post"
  ).length;
  return count;
};

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
          // if (g_outline_id != a_outline_id) return; // attempt to prevent slow loads from overwriting the current outline
          outline_store.set({
            id: a_outline_id,
            ...data,
          });
          get_unread_counts(a_outline_id);

          jquery("#content").scrollTop(0);
          posts_store.current_id.set(null);
          if (data.posts.length > 0) {
            posts_store.set(data.posts);
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
  (a_outline_id, on_success, on_failure) => {
    if (!a_outline_id) return;

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    let skip = count_visible_unread_posts();

    api_request(
      "get_posts",
      { outline: a_outline_id, skip: skip, limit: g_limit },
      function (data) {
        if (!data.error) {
          if (data.posts.length > 0) {
            posts_store.append(data.posts);
            posts_store.no_more_posts.set(false);
            if (on_success) on_success();
          } else {
            posts_store.no_more_posts.set(true);
            if (on_failure) on_failure();
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
  (outline_id) => {
    api_request("get_unread", { outline_id: outline_id }, (data) => {
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
