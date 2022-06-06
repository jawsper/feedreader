<script lang="ts">
  import { options, outlines, outline_id } from "./stores";

  import NavigationLine from "./NavigationLine.svelte";
  import { load_navigation, set_outline_param } from "./api";
  import { onMount } from "svelte";

  const handleOpenFolder = ({ detail }) => {
    const { id: outline_id, folder_opened } = detail;
    set_outline_param(outline_id, "folder_opened", !folder_opened, true);
    outlines.update((outlines) => {
      return outlines.map((outline) => {
        if (outline.id === outline_id) {
          return { ...outline, folder_opened: !folder_opened };
        }
        return outline;
      });
    });
  };

  const handleOpenOutline = ({ detail }) => {
    const { id } = detail;
    const href = `outline/${id}/`;
    outline_id.set(id);
    history.pushState(null, null, href);
  };

  onMount(() => {
    load_navigation();
  });
</script>

<ul
  id="outlines"
  class="feeds"
  class:show-only-unread={$options.show_only_unread.value}
>
  {#each $outlines as outline}
    <NavigationLine
      {outline}
      on:outline
      on:folder-open={handleOpenFolder}
      on:open-outline={handleOpenOutline}
    />
  {/each}
</ul>
