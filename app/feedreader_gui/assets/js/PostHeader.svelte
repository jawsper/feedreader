<script lang="ts">
  import { outline } from "./stores";
</script>

<h3 id="outline_title">
  {#if $outline}
    <a href={$outline.html_url} target="_blank">
      {$outline.title}
    </a>
  {/if}
</h3>
