<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import type { Outline } from "./api/gen";
  import type { FolderOpen, OpenOutline } from "./types";

  export let outline: Outline;
  export let highlight: number | null;

  const dispatch = createEventDispatcher<{
    folder_open: FolderOpen;
    open_outline: OpenOutline;
  }>();

  $: outlineStyle = outline.feed?.icon && `background-image: url(${outline.feed.icon})`;

  const handleOpenFolder = () => {
    if (outline.feed?.id) return;
    dispatch("folder_open", {
      id: outline.id,
      open: outline.folder_opened,
    });
  };
  const handleOpenOutline = () => {
    dispatch("open_outline", { id: outline.id });
  };
</script>

<li
  class="outline"
  class:feed={outline.feed?.id}
  class:folder-closed={!outline.folder_opened}
  class:has-unread={outline.unread_count > 0}
  class:highlight={highlight === outline.id}
>
  <div class="outline-line" style={outlineStyle} on:click={handleOpenFolder} on:keypress={null}>
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
        <svelte:self
          outline={child}
          {highlight}
          on:folder_open
          on:open_outline
        />
      {/each}
    </ul>
  {/if}
</li>
