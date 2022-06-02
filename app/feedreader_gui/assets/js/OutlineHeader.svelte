<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";

  import {
    mark_all_as_read,
    set_outline_param,
    load_posts,
    load_navigation,
  } from "./api";
  import Options from "./Options.svelte";
  import {
    outline_id,
    outline,
    posts,
    header_offsets,
    outlines,
  } from "./stores";
  const { loading } = posts;

  const dispatch = createEventDispatcher();

  let navbar: HTMLDivElement;
  onMount(() => {
    header_offsets.update((value) => ({
      ...value,
      height: navbar.getBoundingClientRect().height,
    }));
  });
</script>

<div class="d-block navbar-right-half" bind:this={navbar}>
  <div class="navbar navbar-expand-sm navbar-light global-header">
    <div class="collapse navbar-collapse content-max">
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
            disabled={$outlines.loading}
            on:click={() => {
              load_navigation();
            }}
          >
            <i class="bi bi-arrow-clockwise" />
            Refresh navigation
          </button>
          <button
            class="btn btn-outline-dark"
            type="button"
            disabled={$loading}
            on:click={() => {
              load_posts($outline_id);
            }}
          >
            <i class="bi bi-arrow-clockwise" />
            Refresh posts
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
            {#if $outline?.sort_order === "asc"}
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
        <span class="navbar-text"
          >Welcome, {document.body.dataset.username} |</span
        >
        <div class="nav-item dropdown">
          <a
            class="nav-link dropdown-toggle"
            data-bs-toggle="dropdown"
            href={"#"}
            role="button"
            aria-expanded="false">Display options</a
          >
          <ul class="dropdown-menu">
            <Options />
          </ul>
        </div>
        <div class="btn-group ms-3">
          <button
            class="nav-item btn btn-outline-dark"
            data-bs-toggle="modal"
            data-bs-target="#new-feed-modal"
          >
            Add a new feed
          </button>
          <a
            class="nav-item btn btn-outline-dark"
            href={document.body.dataset.manageUrl}
          >
            <i class="bi bi-gear" />
            Manage
          </a>
          <a
            class="btn btn-outline-dark"
            href={document.body.dataset.logoutUrl}
          >
            <i class="bi bi-box-arrow-left" />
            Logout
          </a>
        </div>
        <div class="nav-item btn-group ms-3">
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
</div>
