<script lang="ts">
  import { outline } from "./stores";
</script>

<h4 class="mb-3">
  {#if $outline}
    <a href={$outline.feed?.html_url} target="_blank">
      {$outline.title}
    </a>
  {/if}
</h4>
