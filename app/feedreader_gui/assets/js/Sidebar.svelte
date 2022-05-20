<script>
  import { onMount } from "svelte";
  import jquery from "jquery";

  import Options from "./Options";

  let show_options = false;

  onMount(() => {
    jquery("#button-options").button({
      icon: "ui-icon-caret-1-s",
    });
    jquery("#button-refresh-page").button({
      icon: "ui-icon-refresh"
    })
  });
</script>

<p>
  <button id="button-new-feed">Add a new feed</button>
</p>
<p>
  <button
    id="button-options"
    on:click={() => {
      show_options = !show_options;

      jquery("#button-options").button("option", "icons", {
        primary: show_options ? "ui-icon-caret-1-n" : "ui-icon-caret-1-s",
      });
    }}>Options</button
  >
  <button id="button-refresh-page">Refresh</button>
</p>
{#if show_options}
  <Options />
{/if}
