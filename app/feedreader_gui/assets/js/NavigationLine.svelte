<script>
  export let outline;

  import { createEventDispatcher } from "svelte";
  import { set_outline_param } from "./api";

  const dispatch = createEventDispatcher();

  $: outlineClasses = `outline ${outline.feed_id ? "feed" : "folder"} ${
    !outline.folder_opened && "folder-closed"
  } ${outline.unread_count > 0 && "has-unread"}`;

  $: outlineStyle = outline.icon && `background-image: url(${outline.icon})`;

  const handleOpenFolder = () => {
    if (outline.feed_id) return;
    dispatch("folder-open", {
      id: outline.id,
      folder_opened: outline.folder_opened,
    });
  };
  const handleOpenOutline = () => {
    dispatch("open-outline", { id: outline.id });
  };
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
      on:click|preventDefault|stopPropagation={handleOpenOutline}
      >{outline.title}</a
    >
    <span class="outline-unread-count" id="outline-unread-count-{outline.id}"
      >{outline.unread_count}</span
    >
  </div>
  {#if outline.children}
    <ul>
      {#each outline.children as child}
        <svelte:self outline={child} on:folder-open on:open-outline />
      {/each}
    </ul>
  {/if}
</li>
