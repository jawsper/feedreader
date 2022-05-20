<script>
  import { outlines } from "./stores";

  import NavigationLine from "./NavigationLine.svelte";
</script>

{#each $outlines.outlines as outline}
  <NavigationLine {outline} on:outline />
{/each}
