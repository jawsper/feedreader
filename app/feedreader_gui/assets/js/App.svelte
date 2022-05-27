<script lang="ts">
  import { onMount } from "svelte";

  import Navigation from "./Navigation.svelte";
  import NewFeed from "./NewFeed.svelte";
  import OutlineHeader from "./OutlineHeader.svelte";
  import Posts from "./Posts.svelte";
  import Sidebar from "./Sidebar.svelte";
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
    }
  };

  onMount(() => {
    url_change(location.pathname);
  });

  const body = document.querySelector("body");
</script>

<svelte:window on:popstate={() => url_change(location.pathname)} />
<svelte:body on:keypress={on_body_keypress} />

<Toast />
<NewFeed />

<div class="container-fluid">
  <div class="row">
    <div
      class="col-sm-2 position-fixed overflow-auto top-0 bottom-0 pt-2"
      class:d-none={$fullscreen}
    >
      <h2>Feedreader</h2>
      <p>
        Welcome, {body.dataset.username} [<a href={body.dataset.manageUrl}
          >manage</a
        >] [<a href={body.dataset.logoutUrl}>Logout</a>]
      </p>
      <Sidebar />
      <Navigation />
      <div class="position-fixed bottom-0 p-2 fs-6">
        <a target="_blank" href="https://github.com/jawsper/feedreader"
          >Feedreader</a
        >
        v{body.dataset.version}
      </div>
    </div>
    <div class="col-sm-2" class:d-none={$fullscreen} />
    <div class:col-sm-10={!$fullscreen} class="position-relative">
      <OutlineHeader
        on:toggle-fullscreen={() => {
          $fullscreen = !$fullscreen;
        }}
      />
      <div id="content" tabindex="0">
        <Posts on:read={on_posts_read} on:starred={on_posts_starred} />
      </div>
    </div>
  </div>
</div>
