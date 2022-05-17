<script>
  import { createEventDispatcher } from "svelte";
  import { posts } from "./stores";

  export let is_feed;

  const dispatch = createEventDispatcher();

  let posts_value;
  let current_post_id_value;

  posts.subscribe((value) => {
    posts_value = value;
  });
  posts.current_id.subscribe((value) => {
    current_post_id_value = value;
  });

  import Post from "./Post.svelte";

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
</script>

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
