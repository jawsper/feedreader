<script>
  import jquery from "jquery";
  import { onMount } from "svelte";
  import { api_request } from "./api";

  let value = "";

  const add_new_feed = (url) => {
    api_request("feed_add", { url }, (result) => {
      if (result.success) {
        location.reload();
      }
    });
  };

  onMount(() => {
    const dialog = jquery("#new-feed-popup");
    dialog.dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Add feed": () => {
          add_new_feed(value);
        },
        Cancel: function () {
          dialog.dialog("close");
        },
      },
      close: function () {
        jquery("#new-feed-url").val("");
      },
    });
  });
</script>

<label for="new-feed-url"
  >URL: <input id="new-feed-url" type="text" bind:value /></label
>
