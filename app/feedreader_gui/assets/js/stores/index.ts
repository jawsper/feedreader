import { writable } from "svelte/store";

export const load_more_posts = writable<boolean>(false);
export const fullscreen = writable<boolean>(false);

export { toasts } from "./toast";
export { posts } from "./posts";
export { options } from "./options";
export { outlines } from "./outlines";
export { outline_id, outline, unreadPosts } from "./outline";
