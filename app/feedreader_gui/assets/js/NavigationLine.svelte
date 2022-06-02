<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { options } from "./stores";

  import type { IOutline } from "./types";

  export let outline: IOutline;

  const dispatch = createEventDispatcher();

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

  $: visible = !$options.show_only_unread.value || outline.unread_count > 0;
</script>

{#if visible}
  <li
    class="outline"
    class:feed={outline.feed_id}
    class:folder-closed={!outline.folder_opened}
    class:has-unread={outline.unread_count > 0}
  >
    <div class="outline-line" style={outlineStyle} on:click={handleOpenFolder}>
      <a
        class="outline-text"
        href="outline/{outline.id}/"
        on:click|preventDefault|stopPropagation={handleOpenOutline}
      >
        {outline.title}
      </a>
      <span class="outline-unread-count">{outline.unread_count}</span>
    </div>
    {#if outline.children}
      <ul>
        {#each outline.children as child}
          <svelte:self outline={child} on:folder-open on:open-outline />
        {/each}
      </ul>
    {/if}
  </li>
{/if}
