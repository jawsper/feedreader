<script lang="ts">
  import { onMount } from "svelte";

  import Navigation from "./Navigation.svelte";
  import NewFeed from "./NewFeed.svelte";
  import OutlineHeader from "./OutlineHeader.svelte";
  import Posts from "./Posts.svelte";
  import Sidebar from "./Sidebar.svelte";
  import Toast from "./Toast.svelte";

  import { load_more_posts, posts, outline_id } from "./stores";
  import {
    load_more_posts as api_load_more_posts,
    load_posts,
    set_post_attr_state,
  } from "./api";

  load_more_posts.subscribe((more) => {
    if (more) {
      load_more_posts.set(false);
      api_load_more_posts();
    }
  });

  const on_toggle_fullscreen = () => {
    const body = document.querySelector("body");
    const fullscreen = body.classList.toggle("fullscreen");
    if (fullscreen) {
      document.querySelector<HTMLElement>("#content").focus();
    }
  };

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
        load_posts($outline_id);
        break;
      case "j":
        posts.move_post(+1);
        break;
      case "k":
        posts.move_post(-1);
        break;
      case "f":
        on_toggle_fullscreen();
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

  const url_change = (url) => {
    const m = url.match(/\/outline\/(\d+)\//);
    if (m) {
      outline_id.set(parseInt(m[1], 10));
    }
  };
  const on_window_popstate = (e) => {
    url_change(location.pathname);
  };

  onMount(() => {
    url_change(location.pathname);
  });

  const body = document.querySelector("body");
</script>

<svelte:window on:popstate={on_window_popstate} />
<svelte:body on:keypress={on_body_keypress} />

<div id="toast">
  <Toast />
</div>
<div id="new-feed-popup" class="ui-helper-hidden" title="Add new feed">
  <NewFeed />
</div>
<div id="navigation" class="left col scroll-y">
  <h1>Feedreader</h1>
  <p>
    Welcome, {body.dataset.username} [<a href={body.dataset.manageUrl}>manage</a
    >] [<a href={body.dataset.logoutUrl}>Logout</a>]
  </p>
  <div id="sidebar">
    <Sidebar />
  </div>
  <ul id="outlines" class="feeds">
    <Navigation />
  </ul>
</div>
<div id="body" class="right col">
  <div class="content_header row">
    <OutlineHeader on:toggle-fullscreen={on_toggle_fullscreen} />
  </div>
  <div id="content" class="content row scroll-y" tabindex="0">
    <Posts on:read={on_posts_read} on:starred={on_posts_starred} />
  </div>
</div>
