import { debounce } from "lodash";
import { get } from "svelte/store";

import { api } from "./base";
import {
  posts as posts_store,
  outline as outline_store,
  outlines as outlines_store,
  unreadPosts,
} from "../stores";
import type { Outline } from "../api/gen";

export const load_posts = debounce(
  async (a_outline_id: number) => {
    if (!a_outline_id) {
      posts_store.set([]);
      return;
    }

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    try {
      const outline = await api.retrieveSingleOutline({
        id: `${a_outline_id}`,
      });

      const data = await api.listPosts({
        outlinePk: `${a_outline_id}`,
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

      outline_store.set(outline);

      posts_store.current_id.set(null);
      if (data.results.length > 0) {
        posts_store.set(data.results);
      } else {
        posts_store.set([]);
      }
      posts_store.no_more_posts.set(data.next === null);
    } finally {
      posts_store.loading.set(false);
    }
  },
  500,
  { leading: true }
);

export const load_more_posts = debounce(
  async () => {
    const outline = get(outline_store);
    if (!outline) return;
    const { id: outline_id } = outline;

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    let skip = get(unreadPosts);

    try {
      const data = await api.listPosts({
        outlinePk: `${outline_id}`,
        offset: skip,
      });
      if (data.results.length > 0) {
        posts_store.append(data.results);
      }
      posts_store.no_more_posts.set(data.next === null);
    } finally {
      posts_store.loading.set(false);
    }
  },
  500,
  { leading: true }
);

export const get_unread_counts = debounce(
  async () => {
    const outline = get(outline_store);
    if (!outline) return;
    const { id: outline_id } = outline;
    try {
      const data = await api.retrieveUnreadCount({ id: `${outline_id}` });
      document.title =
        data.total > 0 ? `Feedreader (${data.total})` : "Feedreader";
      if (!data.counts) return;

      const update_outline = (outline: Outline) => {
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
    } finally {
    }
  },
  500,
  { trailing: true }
);

export const set_post_attr_state = async (
  post_id: number,
  attr: "read" | "starred",
  state: boolean
) => {
  try {
    const data = await api.partialUpdatePost({
      postId: `${post_id}`,
      post: {
        [attr]: state,
      },
    });
    if (data) get_unread_counts();
  } finally {
  }
};
