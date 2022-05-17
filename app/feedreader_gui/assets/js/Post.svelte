<script>
  import DOMPurify from "dompurify";
  import { createEventDispatcher } from "svelte";

  DOMPurify.addHook("afterSanitizeAttributes", (node) => {
    if (node.tagName === "A") {
      node.setAttribute("target", "_blank");
      node.setAttribute("rel", "noreferrer noopener");
      node.setAttribute("referrerpolicy", "no-referrer");
    }
    return node;
  });

  import { posts } from "./stores"


  export let post;
  export let is_feed;
  export let is_current;

  const dispatch = createEventDispatcher();

  let div;
  let dont_auto_mark_read = false;
  $: is_starred = post.starred;
  $: is_read = post.read;

  posts.current_id.subscribe(new_id => {
    if(new_id === post.id) {
      div.scrollIntoView(true);
      if (!dont_auto_mark_read && !is_read) {
        mark_post_read();
      }
    }
  })

  $: postClasses = `post ${is_current ? "current" : ""}`;

  const mark_post_starred = () => {
    dispatch("starred", {
      id: post.id,
      value: !is_starred,
    });
  };
  const mark_post_read = () => {
    const new_is_read = !is_read;
    if (!new_is_read) {
      dont_auto_mark_read = true;
    }
    dispatch("read", {
      id: post.id,
      value: new_is_read,
    });
  };
</script>

<div
  bind:this={div}
  class={postClasses}
  id="post_{post.id}"
  on:mouseup={dispatch("focus", post.id)}
>
  <div class="body">
    <div class="link">
      <a
        href={post.link}
        target="_blank"
        rel="noreferrer noopener"
        referrerpolicy="no-referrer">{post.title}</a
      >
    </div>
    <div class="pubDate">{post.pubDate}</div>
    <div class="source">
      {#if !is_feed}
        from {post.feedTitle}
      {/if}
      {#if post.author}
        by <span class="authorName">{post.author}</span>
      {/if}
    </div>
    <br />
    <div class="content">
      {@html DOMPurify.sanitize(post.content)}
    </div>
  </div>
  <div class="footer">
    <label for="cb_action_starred_post_{post.id}">
      <input
        id="cb_action_starred_post_{post.id}"
        class="action starred"
        type="checkbox"
        name="starred"
        value="1"
        bind:checked={is_starred}
        on:click={mark_post_starred}
      />
      Starred
    </label>
    <label for="cb_action_read_post_{post.id}">
      <input
        id="cb_action_read_post_{post.id}"
        class="action read"
        type="checkbox"
        name="read"
        value="1"
        bind:checked={is_read}
        on:click={mark_post_read}
      />
      Mark as read
    </label>
  </div>
</div>
