import { writable } from "svelte/store";

export const outline = writable(null);
export const load_more_posts = writable(false);

export const toast = writable(null);
export { posts } from "./posts";
export { outlines } from "./outlines";
