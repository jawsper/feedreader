import { writable } from "svelte/store";
import type { IOutline } from "../types";

const initial_outlines = JSON.parse(document.getElementById("navigation").textContent);

export const outlines = writable<IOutline[]>(initial_outlines);
export const outlines_loading = writable<boolean>(false);
