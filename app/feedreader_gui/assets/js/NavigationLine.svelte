<script>
  export let outline;

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  $: outlineClasses = `outline ${outline.feed_id ? "feed" : "folder"} ${
    !outline.folder_opened && "folder-closed"
  } ${outline.unread_count > 0 && "has-unread"}`;

  $: outlineStyle = outline.icon && `background-image: url(${outline.icon})`;

  function handleOpenFolder(e) {
    if (outline.feed_id) return;
    console.log("handleOpenFolder", e);
  }
  function handleOpenOutline(e) {
    console.log("handleClick", e);
    e.preventDefault();
    const url = e.target.href;
    console.log(url, outline.id);
    dispatch("outline", outline.id);
  }
</script>

<li
  id="outline-{outline.id}"
  data-unread-count={outline.unread_count}
  class={outlineClasses}
>
  <div class="outline-line" style={outlineStyle} on:click={handleOpenFolder}>
    <a
      class="outline-text"
      href="outline/{outline.id}/"
      on:click={handleOpenOutline}>{outline.title}</a
    >
    <span class="outline-unread-count" id="outline-unread-count-{outline.id}"
      >{outline.unread_count}</span
    >
  </div>
  {#if outline.children}
    <ul>
      {#each outline.children as child}
        <svelte:self outline={child} />
      {/each}
    </ul>
  {/if}
</li>
