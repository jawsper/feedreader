<script lang="ts">
  import { outline } from "./stores";
</script>

<h4 class="my-3">
  {#if $outline}
    <a href={$outline.html_url} target="_blank">
      {$outline.title}
    </a>
  {/if}
</h4>
