<script lang="ts">
  import { onMount } from "svelte";

  import Options from "./Options.svelte";

  import { outlines } from "./stores";
  import { load_navigation } from "./api/outline";

  let show_options = false;
  let loading = false;
  outlines.subscribe((data) => {
    loading = data.loading;
  });

  onMount(() => {
    load_navigation();
  });
</script>

<p>
  <button
    class="btn btn-outline-dark"
    data-bs-toggle="modal"
    data-bs-target="#new-feed-modal"
  >
    Add a new feed
  </button>
</p>
<p>
  <button
    id="button-options"
    class="ui-button ui-corner-all ui-widget"
    on:click={() => {
      show_options = !show_options;
    }}
  >
    <span
      class={`ui-button-icon ui-icon ui-icon-caret-1-${
        show_options ? "n" : "s"
      }`}
    />
    <span class="ui-button-icon-space" />
    Options
  </button>
  <button
    id="button-refresh-page"
    class={`ui-button ui-corner-all ui-widget ${
      loading && "ui-button-disabled ui-state-disabled"
    }`}
    on:click={load_navigation}
  >
    <span class="ui-button-icon ui-icon ui-icon-refresh" />
    <span class="ui-button-icon-space" />
    Refresh
  </button>
</p>
<Options visible={show_options} />
