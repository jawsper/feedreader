import { writable } from "svelte/store";
import type { Outline } from "../api/gen";

const initial_outlines = JSON.parse(document.getElementById("navigation").textContent);

export const outlines = writable<Outline[]>(initial_outlines);
export const outlines_loading = writable<boolean>(false);
