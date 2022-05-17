<script>
  import { outline } from "./stores";

  let outline_data;
  outline.subscribe(($outline) => {
    outline_data = $outline;
  });
</script>

<button id="button_toggle_fullscreen" title="Toggle fullscreen">
  <span class="ui-icon ui-icon-arrow-4-diag" />
</button>
<button id="button_refresh" title="Refresh">
  <span class="ui-icon ui-icon-refresh" />
</button>
<button id="button_mark_all_as_read">Mark all as read</button>
<button id="button_show_only_new">
  {#if outline_data?.show_only_new}
  {outline_data.unread_count} new item{#if outline_data.unread_count !== 1}s{/if}
  {:else if outline_data}
  All items
  {:else}
  &nbsp;
  {/if}
</button>
<button id="button_sort_order">
  {#if outline_data?.sort_order === "ASC"}
  Oldest first
  {:else if outline_data}
  Newest first
  {:else}
  &nbsp;
  {/if}
</button>
<div style="float:right">
  <button id="button_prev_post" title="Previous post">
    <span class="ui-icon ui-icon-triangle-1-n" />
  </button>
  <button id="button_next_post" title="Next post">
    <span class="ui-icon ui-icon-triangle-1-s" />
  </button>
</div>
