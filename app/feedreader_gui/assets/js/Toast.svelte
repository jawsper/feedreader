<script>
  import { afterUpdate } from "svelte/internal";
  import { fade } from "svelte/transition"

  import { toast } from "./stores";

  $: classNames = $toast?.success ? "ui-state-highlight" : "ui-state-error";
  $: icon = $toast?.success ? "ui-icon-info" : "ui-icon-alert";

  let timeout;

  afterUpdate(() => {
    if(timeout) clearTimeout(timeout)
    timeout = setTimeout(() => {
        $toast = null
    }, 5000)
  });
</script>

{#if $toast}
  <div id="result" class="ui-widget" transition:fade>
    <div id="result_container" class={`ui-corner-all ${classNames}`}>
      <p>
        <span id="result_icon" class={`ui-icon ${icon}`} />
        {#if $toast.caption}
          <strong id="result_caption">
            <span id="result_caption_text">{$toast.caption}</span>:
          </strong>
        {/if}
        <span id="result_text">{$toast.message}</span>
      </p>
    </div>
  </div>
{/if}
