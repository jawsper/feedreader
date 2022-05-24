import { derived, writable } from "svelte/store";
import { load_posts } from "../api/posts";
import { posts } from "./posts";

export const outline_id = writable(null);

const createOutline = () => {
  const { subscribe, set, update } = writable(null);

  outline_id.subscribe(($outline_id) => {
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
  const { show_only_new } = outline;
  // get all unread posts and skip those
  // or just all posts
  return posts.filter((post) => (show_only_new ? !post.read : true)).length;
});
