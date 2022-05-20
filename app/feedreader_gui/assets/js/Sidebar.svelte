<script>
  import { onMount } from "svelte";
  import jquery from "jquery";

  import { api_request } from "./api";
  import { outlines } from "./stores";
  import Options from "./Options";

  let show_options = false;

  const load_navigation = () => {
    outlines.update(($outline) => ({
      ...$outline,
      loading: true,
    }));
    api_request("outline_get_all_outlines", {}, (data) => {
      $outlines = {
        loading: false,
        outlines: data.outlines,
      };
    });
  };

  outlines.subscribe((data) => {
    jquery("#button-refresh-page").button("option", "disabled", data.loading);
  });

  onMount(() => {
    jquery("#button-options").button({
      icon: "ui-icon-caret-1-s",
    });
    jquery("#button-refresh-page").button({
      icon: "ui-icon-refresh",
    });

    load_navigation();
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
  <button id="button-refresh-page" on:click={load_navigation}>Refresh</button>
</p>
{#if show_options}
  <Options />
{/if}
