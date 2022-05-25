import { writable } from "svelte/store";

import type { IToast } from "../types";

export const load_more_posts = writable<boolean>(false);

export const toast = writable<IToast | null>(null);
export { posts } from "./posts";
export { outlines } from "./outlines";
export { outline_id, outline, unreadPosts } from "./outline";
