<script lang="ts">
  import DOMPurify from "dompurify";
  import { formatRelative } from "date-fns";
  import { createEventDispatcher } from "svelte";
  import { locale } from "./utils/locale";

  import type { Post } from "./api/gen";
  import type { PostFocus, PostRead, PostStarred } from "./types";

  DOMPurify.addHook("afterSanitizeAttributes", (node) => {
    if (node.tagName === "A") {
      node.setAttribute("target", "_blank");
      node.setAttribute("rel", "noreferrer noopener");
      node.setAttribute("referrerpolicy", "no-referrer");
    }
    return node;
  });

  import { header_offset, posts } from "./stores";

  export let post: Post;
  export let is_feed: boolean;
  export let is_current: boolean;

  const dispatch = createEventDispatcher<{
    starred: PostStarred,
    read: PostRead,
    focus: PostFocus,
  }>();

  let div: HTMLDivElement;
  let dont_auto_mark_read = false;
  $: is_starred = post.starred;
  $: is_read = post.read;

  posts.current_id.subscribe((new_id) => {
    if (div && new_id === post.id) {
      const offset = div.getBoundingClientRect().top;
      const top = offset + window.pageYOffset - $header_offset;
      window.scrollTo({
        top,
        // @ts-ignore
        behavior: "instant",
      });
      if (!dont_auto_mark_read && !is_read) {
        mark_post_read();
      }
    }
  });

  $: postClasses = `post ${is_current ? "current" : ""}`;

  const mark_post_starred = () => {
    dispatch("starred", {
      id: post.id,
      starred: !is_starred,
    });
  };
  const mark_post_read = () => {
    const new_is_read = !is_read;
    if (!new_is_read) {
      dont_auto_mark_read = true;
    }
    dispatch("read", {
      id: post.id,
      read: new_is_read,
    });
  };

  const format_date = (date: Date) => {
    return formatRelative(date, new Date(), { locale, weekStartsOn: 1 });
  }
</script>

<div
  bind:this={div}
  class={postClasses}
  id="post_{post.id}"
  on:mouseup={() => dispatch("focus", {id: post.id })}
>
  <div class="header">
    <div class="link">
      <a
        href={post.link}
        target="_blank"
        rel="noreferrer noopener"
        referrerpolicy="no-referrer">{post.title}</a
      >
    </div>
    <div class="pubDate" title={post.pub_date?.toString()}>{format_date(post.pub_date)}</div>
    <div class="source">
      {#if !is_feed}
        from {post.feed_title}
      {/if}
      {#if post.author}
        by <span class="authorName">{post.author}</span>
      {/if}
    </div>
  </div>
  <div class="body">
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
