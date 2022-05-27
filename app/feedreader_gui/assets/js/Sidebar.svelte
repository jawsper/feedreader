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
<div class="btn-group mb-3">
  <button
    class="btn btn-outline-dark"
    on:click={() => {
      show_options = !show_options;
    }}
  >
    <i class={`bi bi-caret-${show_options ? "up" : "down"}-fill`} />
    Options
  </button>
  <button
    class="btn btn-outline-dark"
    disabled={loading}
    on:click={load_navigation}
  >
    <i class="bi bi-arrow-clockwise" />
    Refresh
  </button>
</div>
<Options visible={show_options} />
