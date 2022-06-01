<script lang="ts">
  import { slide } from "svelte/transition";

  import { toasts } from "./stores";
</script>

<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
  <div class="toast-container">
    {#each $toasts as toast}
      <div
        class="toast show"
        role="alert"
        class:bg-primary={toast.success}
        class:bg-danger={!toast.success}
        transition:slide
      >
        <div class="toast-header">
          <i
            class="bi me-2"
            class:text-primary={toast.success}
            class:text-danger={!toast.success}
            class:bi-info-square-fill={toast.success}
            class:bi-exclamation-square-fill={!toast.success}
          />
          <strong class="me-auto">{toast.caption}</strong>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="toast"
            aria-label="Close"
          />
        </div>
        <div class="toast-body">
          {toast.message}
        </div>
      </div>
    {/each}
  </div>
</div>
