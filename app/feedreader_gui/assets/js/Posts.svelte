<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import InfiniteScroll from "svelte-infinite-scroll";

  import { header_offsets, outline, posts } from "./stores";
  const { current_id, loading, no_more_posts } = posts;

  import { load_more_posts } from "./api";
  import Post from "./Post.svelte";
  import PostHeader from "./PostHeader.svelte";
  import type { PostFocus, PostRead, PostStarred } from "./types";

  const dispatch = createEventDispatcher<{
    starred: PostStarred,
    read: PostRead,
  }>();

  const post_on_focus = (e: CustomEvent<PostFocus>) => {
    const { id } = e.detail;
    $current_id = id;
  };

  const post_on_starred = (e: CustomEvent<PostStarred>) => {
    const { id, starred } = e.detail;
    posts.update_post(id, { starred });
    dispatch("starred", e.detail);
  };

  const post_on_read = (e: CustomEvent<PostRead>) => {
    const { id, read } = e.detail;
    posts.update_post(id, { read });
    dispatch("read", e.detail);
  };

  let section: HTMLElement;

  onMount(() => {
    header_offsets.update((value) => ({
      ...value,
      padding: parseFloat(
        window.getComputedStyle(section, null).getPropertyValue("padding-top")
      ),
    }));
  });
</script>

<InfiniteScroll
  threshold={100}
  window={true}
  hasMore={!$no_more_posts}
  on:loadMore={() => {
    if (!$loading) load_more_posts();
  }}
/>

<section class="pt-3 px-3 content-max prose" bind:this={section}>
  <PostHeader />
  <div id="posts">
    {#each $posts as post}
      <Post
        {post}
        is_feed={$outline?.feed !== undefined}
        is_current={$current_id === post.id}
        on:focus={post_on_focus}
        on:starred={post_on_starred}
        on:read={post_on_read}
      />
    {/each}
  </div>
  <div class="container-fluid mb-3">
    <div class="row align-items-center">
      <div class="col-md-auto">
        <button
          class="btn btn-outline-primary"
          disabled={$loading}
          on:click={load_more_posts}
        >
          Load more posts
        </button>
      </div>
      {#if $no_more_posts}
        <div class="col-md-auto">No more posts.</div>
      {/if}
    </div>
  </div>
</section>
