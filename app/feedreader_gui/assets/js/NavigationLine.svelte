<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import type { Outline } from "./api/gen";

  export let outline: Outline;
  export let highlight: number | null;

  const dispatch = createEventDispatcher();

  $: outlineStyle = outline.feed?.icon && `background-image: url(${outline.feed.icon})`;

  const handleOpenFolder = () => {
    if (outline.feed?.id) return;
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
  class="outline"
  class:feed={outline.feed?.id}
  class:folder-closed={!outline.folder_opened}
  class:has-unread={outline.unread_count > 0}
  class:highlight={highlight === outline.id}
>
  <div class="outline-line" style={outlineStyle} on:click={handleOpenFolder}>
    <a
      class="outline-text"
      href="outline/{outline.id}/"
      on:click|preventDefault|stopPropagation={handleOpenOutline}
      title={outline.title}
    >
      {outline.title}
    </a>
    <span class="outline-unread-count">{outline.unread_count}</span>
  </div>
  {#if outline.children}
    <ul>
      {#each outline.children as child}
        <svelte:self outline={child} {highlight} on:folder-open on:open-outline />
      {/each}
    </ul>
  {/if}
</li>
