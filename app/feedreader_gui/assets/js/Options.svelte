<script>
  import jquery from "jquery";
  import { onMount } from "svelte";
  import { api_request } from "./api";

  const options = {
    show_only_unread: {
      title: "Show only unread posts",
      type: "boolean",
      default: false,
      callback: function () {
        // TODO: svelte this
        jquery("#outlines").toggleClass("show-only-unread", this.value);
      },
    },
    show_nsfw_feeds: {
      title: "Show NSFW feeds",
      type: "boolean",
      default: false,
      callback: () => {
        // TODO: svelte this
        jquery("#button_refresh_page").trigger("click");
        jquery("#button_refresh").trigger("click");
      },
    },
  };

  onMount(() => {
    jquery(".option-button").button({
      icons: { primary: "ui-icon-circle-check" },
    });
    load_options();
  });

  const load_options = () => {
    const opts = Object.keys(options);
    api_request("get_option", { keys: opts }, (result) => {
      for (const [name, data] of Object.entries(options)) {
        if (typeof result.options[name] == "undefined") {
          // key not found
          data.value = data.default;
        } else {
          data.value = result.options[name];
        }
        if (data.type === "boolean") {
          const icon = data.value
            ? "ui-icon-circle-check"
            : "ui-icon-circle-close";
          jquery(`#btn-option-${name}`).button("option", "icons", {
            primary: icon,
          });
        }
        if (data.callback) data.callback.apply(data);
      }
    });
  };

  const save_option = (name, value) => {
    const data = {
      [name]: value,
    };
    api_request("set_option", data, (result) => {
      if (result.success) {
        load_options();
      }
    });
  };

  const option_button_click = (name) => {
    const option = options[name];
    if (option.type === "boolean") {
      option.value = !option.value;
      save_option(name, option.value);
      const icon = option.value
        ? "ui-icon-circle-check"
        : "ui-icon-circle-close";
      jquery(`#btn-option-${name}`).button("option", "icons", {
        primary: icon,
      });
    }
  };
</script>

{#each Object.entries(options) as [name, option]}
  <li>
    <button
      class="option-button"
      id={`btn-option-${name}`}
      on:click={() => option_button_click(name)}
    >
      {option.title}
    </button>
  </li>
{/each}
