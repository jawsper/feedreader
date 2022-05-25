<script lang="ts">
  import { api_request } from "./api";

  let value = "";

  const add_new_feed = (url: string) => {
    api_request("feed_add", { url }, (result) => {
      if (result.success) {
        location.reload();
      }
    });
  };

  const handle_add_feed = () => {
    add_new_feed(value);
  };
</script>

<div id="new-feed-modal" class="modal fade" tabindex="-1">
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
