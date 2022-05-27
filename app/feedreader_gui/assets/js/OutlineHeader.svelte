<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { mark_all_as_read, set_outline_param, load_posts } from "./api";
  import { outline_id, outline, posts } from "./stores";
  const { loading } = posts;

  const dispatch = createEventDispatcher();
</script>

<nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
  <div class="container-fluid">
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon" />
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <div class="navbar-nav">
        <div class="nav-item btn-group">
          <button
            class="btn btn-outline-dark"
            type="button"
            title="Toggle fullscreen"
            on:click={() => dispatch("toggle-fullscreen")}
          >
            <i class="bi bi-arrows-fullscreen" />
          </button>
          <button
            class="btn btn-outline-dark"
            type="button"
            title="Refresh"
            disabled={$loading}
            on:click={() => {
              load_posts($outline_id);
            }}
          >
            <i class="bi bi-arrow-clockwise" />
          </button>
          <button
            class="btn btn-outline-dark"
            type="button"
            disabled
            on:click={() => {
              if ($outline) mark_all_as_read($outline.id);
            }}
          >
            Mark all as read
          </button>
          <button
            class="btn btn-outline-dark"
            type="button"
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
            class="btn btn-outline-dark"
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
        </div>
      </div>
      <div class="navbar-nav ms-auto">
        <div class="nav-item btn-group">
          <button
            class="btn btn-outline-dark"
            type="button"
            title="Previous post"
            on:click={() => posts.move_post(-1)}
          >
            <i class="bi bi-caret-up-fill" />
          </button>
          <button
            class="btn btn-outline-dark"
            type="button"
            title="Next post"
            on:click={() => posts.move_post(1)}
          >
            <i class="bi bi-caret-down-fill" />
          </button>
        </div>
      </div>
    </div>
  </div>
</nav>
