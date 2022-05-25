<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { outline, posts } from "./stores";
  const { current_id, loading, no_more_posts } = posts;

  import { load_more_posts } from "./api";
  import Post from "./Post.svelte";
  import PostHeader from "./PostHeader.svelte";

  const dispatch = createEventDispatcher();

  const post_on_focus = (e) => {
    const post_id = e.detail;
    $current_id = post_id;
  };

  const post_on_starred = (e) => {
    const { id, value } = e.detail;
    posts.update_post(id, {
      starred: value,
    });
    dispatch("starred", e.detail);
  };

  const post_on_read = (e) => {
    const { id, value } = e.detail;
    posts.update_post(id, {
      read: value,
    });
    dispatch("read", e.detail);
  };
</script>

<PostHeader />
<div id="posts">
  {#each $posts as post}
    <Post
      {post}
      is_feed={$outline.is_feed}
      is_current={$current_id === post.id}
      on:focus={post_on_focus}
      on:starred={post_on_starred}
      on:read={post_on_read}
    />
  {/each}
</div>
{#if !$loading}
  <div id="load_more_posts">
    <button class="button ui-button ui-corner-all ui-widget" on:click={load_more_posts}
      >Load more posts</button
    >
  </div>
{/if}
{#if $no_more_posts}
  <div id="no_more_posts">No more posts.</div>
{/if}
<div style="height: 50%" />