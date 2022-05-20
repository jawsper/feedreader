import { writable } from "svelte/store";

export const load_more_posts = writable(false);

export const toast = writable(null);
export { posts } from "./posts";
export { outlines } from "./outlines";
export { outline_id, outline, unreadPosts } from "./outline";
