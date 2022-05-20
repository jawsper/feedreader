<script>
  import { createEventDispatcher } from "svelte";
  import { posts } from "./stores";

  import Post from "./Post.svelte";
  import PostHeader from "./PostHeader.svelte";

  export let is_feed;

  const dispatch = createEventDispatcher();

  let posts_value;
  let current_post_id_value;
  let loading;
  let no_more_posts;

  posts.subscribe((value) => {
    posts_value = value;
  });
  posts.current_id.subscribe((value) => {
    current_post_id_value = value;
  });
  posts.loading.subscribe((value) => {
    loading = value;
  });
  posts.no_more_posts.subscribe((value) => {
    no_more_posts = value;
  });

  const post_on_focus = (e) => {
    const post_id = e.detail;
    posts.current_id.set(post_id);
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

  $: {
  }

  const load_more_posts = () => {
    dispatch("load_more_posts");
  };
</script>

<PostHeader />
<div id="posts">
  {#each posts_value as post}
    <Post
      {post}
      {is_feed}
      is_current={current_post_id_value === post.id}
      on:focus={post_on_focus}
      on:starred={post_on_starred}
      on:read={post_on_read}
    />
  {/each}
</div>
{#if !loading}
  <div id="load_more_posts">
    <button class="button" on:click={load_more_posts}>Load more posts</button>
  </div>
{/if}
{#if no_more_posts}
<div id="no_more_posts">No more posts.</div>
{/if}
<div style="height: 50%" />
