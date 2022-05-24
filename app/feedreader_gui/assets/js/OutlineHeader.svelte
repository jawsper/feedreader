<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { mark_all_as_read, set_outline_param, load_posts } from "./api";
  import { outline_id, outline, posts } from "./stores";

  const dispatch = createEventDispatcher();
</script>

<button
  id="button_toggle_fullscreen"
  title="Toggle fullscreen"
  on:click={() => dispatch("toggle-fullscreen")}
>
  <span class="ui-icon ui-icon-arrow-4-diag" />
</button>
<button
  id="button_refresh"
  title="Refresh"
  on:click={() => {
    load_posts($outline_id);
  }}
>
  <span class="ui-icon ui-icon-refresh" />
</button>
<button
  id="button_mark_all_as_read"
  on:click={() => {
    if ($outline) mark_all_as_read($outline.id);
  }}>Mark all as read</button
>
<button
  id="button_show_only_new"
  on:click={() => {
    if ($outline) set_outline_param($outline.id, "show_only_new");
  }}
>
  {#if $outline?.show_only_new}
    {$outline.unread_count} new item{#if $outline.unread_count !== 1}s{/if}
  {:else if $outline}
    All items
  {:else}
    &nbsp;
  {/if}
</button>
<button
  id="button_sort_order"
  on:click={() => {
    if ($outline) set_outline_param($outline.id, "sort_order");
  }}
>
  {#if $outline?.sort_order === "ASC"}
    Oldest first
  {:else if $outline}
    Newest first
  {:else}
    &nbsp;
  {/if}
</button>
<div style="float:right">
  <button
    id="button_prev_post"
    title="Previous post"
    on:click={() => posts.move_post(-1)}
  >
    <span class="ui-icon ui-icon-triangle-1-n" />
  </button>
  <button
    id="button_next_post"
    title="Next post"
    on:click={() => posts.move_post(1)}
  >
    <span class="ui-icon ui-icon-triangle-1-s" />
  </button>
</div>
