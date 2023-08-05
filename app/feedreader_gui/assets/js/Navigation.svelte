<script lang="ts">
  import { options, outlines, outline_id } from "./stores";

  import NavigationLine from "./NavigationLine.svelte";
  import { set_outline_param } from "./api";
  import type { Outline } from "./api/gen";
  import type { FolderOpen, OpenOutline } from "./types";

  const handleOpenFolder = ({ detail }: CustomEvent<FolderOpen>) => {
    const { id: outline_id, open } = detail;
    set_outline_param(outline_id, "folder_opened", !open, true);
    outlines.update((outlines) => {
      return outlines.map((outline) => {
        if (outline.id === outline_id) {
          return { ...outline, folder_opened: !open };
        }
        return outline;
      });
    });
  };

  const open_outline = (id: number) => {
    const href = `outline/${id}/`;
    outline_id.set(id);
    history.pushState(null, null, href);
  };

  const handleOpenOutline = ({ detail }: CustomEvent<OpenOutline>) => open_outline(detail.id);

  let highlight: number | null = null;

  const update_highlight = (id: number, next: boolean = true) => {
    const flatten_outline = (outline: Outline): Outline[] => {
      if(outline.children && !outline.folder_opened) return [outline];
      return [outline, ...outline.children.map(flatten_outline)].flat();
    }

    let flattened = $outlines.flatMap(flatten_outline);
    if ($options.show_only_unread.value) {
      flattened = flattened.filter((o) => o.unread_count > 0);
    }
    let idx: number;
    if (id !== null) {
      idx = flattened.findIndex((ol) => ol.id === id);
    } else {
      idx = -1;
    }
    let next_idx = next ? idx + 1 : idx - 1;
    if (next_idx < 0 || next_idx >= flattened.length) {
      next_idx = null;
    }
    if (next_idx !== null) {
      const next_id = flattened[next_idx].id;
      highlight = next_id;
    } else {
      highlight = null;
    }
  };

  export const highlight_prev = () => {
    update_highlight(highlight, false);
  };
  export const highlight_next = () => {
    update_highlight(highlight);
  };
  export const highlight_open = () => {
    if (highlight !== null) {
      open_outline(highlight);
    }
  };
  export const highlight_clear = () => {
    highlight = null;
  };
</script>

<ul
  id="outlines"
  class="feeds"
  class:show-only-unread={$options.show_only_unread.value}
>
  {#each $outlines as outline}
    <NavigationLine
      {outline}
      {highlight}
      on:outline
      on:folder_open={handleOpenFolder}
      on:open_outline={handleOpenOutline}
    />
  {/each}
</ul>
