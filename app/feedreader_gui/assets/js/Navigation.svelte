<script lang="ts">
  import { outlines, outline_id } from "./stores";

  import NavigationLine from "./NavigationLine.svelte";
  import { set_outline_param } from "./api";

  const handleOpenFolder = ({ detail }) => {
    const { id: outline_id, folder_opened } = detail;
    set_outline_param(outline_id, "folder_opened", !folder_opened, true);
    outlines.update(({ outlines, ...rest }) => {
      return {
        ...rest,
        outlines: outlines.map((outline) => {
          if (outline.id === outline_id) {
            return { ...outline, folder_opened: !folder_opened };
          }
          return outline;
        }),
      };
    });
  };

  const handleOpenOutline = ({ detail }) => {
    const { id } = detail;
    const href = `outline/${id}/`;
    outline_id.set(id);
    console.log(id, href)
    history.pushState(null, null, href);
  };
</script>

{#each $outlines.outlines as outline}
  <NavigationLine
    {outline}
    on:outline
    on:folder-open={handleOpenFolder}
    on:open-outline={handleOpenOutline}
  />
{/each}
