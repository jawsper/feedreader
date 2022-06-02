<script lang="ts">
  import { onMount } from "svelte";

  import Navigation from "./Navigation.svelte";
  import NewFeed from "./NewFeed.svelte";
  import OutlineHeader from "./OutlineHeader.svelte";
  import Posts from "./Posts.svelte";
  import Toast from "./Toast.svelte";

  import { load_more_posts, posts, outline_id, fullscreen } from "./stores";
  import {
    load_more_posts as api_load_more_posts,
    load_navigation,
    load_posts,
    set_post_attr_state,
  } from "./api";

  load_more_posts.subscribe((more) => {
    if (more) {
      load_more_posts.set(false);
      api_load_more_posts();
    }
  });

  const on_posts_read = (e) => {
    const { id, value } = e.detail;
    set_post_attr_state(id, "read", value);
  };
  const on_posts_starred = (e) => {
    const { id, value } = e.detail;
    set_post_attr_state(id, "starred", value);
  };

  const on_body_keypress = (e) => {
    let key = e.key.toLowerCase();
    if (e.shiftKey) key = "shift+" + key;
    if (e.metaKey) key = "meta+" + key;
    if (e.ctrlKey) key = "ctrl+" + key;
    if (e.altKey) key = "alt+" + key;
    switch (key) {
      case "r":
        load_navigation();
        load_posts($outline_id);
        break;
      case "j":
        posts.move_post(+1);
        break;
      case "k":
        posts.move_post(-1);
        break;
      case "f":
        $fullscreen = !$fullscreen;
        break;
      case "m":
        posts.update_current_post((post) => {
          set_post_attr_state(post.id, "read", !post.read);
          return {
            ...post,
            read: !post.read,
          };
        });
        break;
      case "s":
        posts.update_current_post((post) => {
          set_post_attr_state(post.id, "starred", !post.starred);
          return {
            ...post,
            starred: !post.starred,
          };
        });
        break;
      case "v":
        posts.current_open_link();
        break;
    }
  };

  const url_change = (url: string) => {
    const m = url.match(/\/outline\/(\d+)\//);
    if (m) {
      outline_id.set(parseInt(m[1], 10));
    } else {
      outline_id.set(null);
    }
  };

  onMount(() => {
    url_change(location.pathname);
  });
</script>

<svelte:window on:popstate={() => url_change(location.pathname)} />
<svelte:body on:keypress={on_body_keypress} />

<Toast />
<NewFeed />

<div class="sidebar">
  <div class="navbar navbar-expand-md navbar-light bg-white global-header">
    <a class="navbar-brand pb-0" title="Feedreader" href="/">
      <h6>Feedreader</h6>
    </a>
  </div>
  <div
    id="sidebar"
    class="d-flex flex-column align-items-stretch collapse navbar-collapse"
    class:d-none={$fullscreen}
  >
    <div class="aside">
      <div class="px-3">
        <Navigation />
      </div>
    </div>
    <div id="version" class="p-2 fs-6">
      <a target="_blank" href="https//github.com/jawsper/feedreader"
        >Feedreader</a
      >
      v{document.body.dataset.version}
    </div>
  </div>
</div>
<main class="px-0" class:fullscreen={$fullscreen}>
  <div class="flex-grow-1">
    <OutlineHeader
      on:toggle-fullscreen={() => {
        $fullscreen = !$fullscreen;
      }}
    />
    <Posts on:read={on_posts_read} on:starred={on_posts_starred} />
  </div>
</main>
