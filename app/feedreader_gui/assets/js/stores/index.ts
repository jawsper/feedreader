import { derived, writable } from "svelte/store";

export const load_more_posts = writable<boolean>(false);
export const fullscreen = writable<boolean>(false);

export const header_offsets = writable({ height: 0, padding: 0 });

export const header_offset = derived(header_offsets, value => value.height + value.padding)

export { toasts } from "./toast";
export { posts } from "./posts";
export { options } from "./options";
export { outlines, outlines_loading } from "./outlines";
export { outline_id, outline, unreadPosts } from "./outline";
