<script>
  export let navigation = [];

  console.log("Navigation.svelte");

  $: {
    console.log(navigation);
  }

  import NavigationLine from "./NavigationLine.svelte";
</script>

{#each navigation as outline}
  <NavigationLine {outline} on:outline />
{/each}
