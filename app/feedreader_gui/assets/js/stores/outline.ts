import { derived, writable } from "svelte/store";
import { load_posts } from "../api/posts";
import { posts } from "./posts";

import type { SingleOutline } from "../api/gen";

export const outline_id = writable<number | null>(null);

const createOutline = () => {
  const { subscribe, set, update } = writable<SingleOutline>(null);

  outline_id.subscribe(($outline_id) => {
    if (!$outline_id) set(null);
    load_posts($outline_id);
  });

  return {
    subscribe,
    set,
    update,
  };
};

export const outline = createOutline();

export const unreadPosts = derived([outline, posts], ([outline, posts]) => {
  // get all unread posts and skip those
  // or just all posts
  return posts.filter((post) => (outline?.show_only_new ? !post.read : true))
    .length;
});
