<script lang="ts">
  import { onMount } from "svelte";
  import { add_new_feed, load_navigation } from "./api";
  import { Modal } from "bootstrap";

  let input: HTMLInputElement, modal: Element;
  let value = "";

  onMount(() => {
    modal.addEventListener("shown.bs.modal", () => {
      input.focus();
    });
    modal.addEventListener("hidden.bs.modal", () => {
      value = "";
    });
  });

  const handle_add_feed = async () => {
    try {
      const result = await add_new_feed(value);
      if (result) {
        Modal.getInstance(modal).hide();
        await load_navigation();
      }
    } finally {
    }
  };
</script>

<div id="new-feed-modal" class="modal fade" tabindex="-1" bind:this={modal}>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add feed</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        />
      </div>
      <div class="modal-body">
        <form on:submit|preventDefault={handle_add_feed}>
          <label for="new-feed-url" class="form-label">URL</label>
          <input
            type="text"
            id="new-feed-url"
            class="form-control"
            bind:this={input}
            bind:value
          />
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"
          >Close</button
        >
        <button type="button" class="btn btn-primary" on:click={handle_add_feed}
          >Add feed</button
        >
      </div>
    </div>
  </div>
</div>
