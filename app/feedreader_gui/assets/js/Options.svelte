<script lang="ts">
  import { cloneDeep } from "lodash";
  import { update_config, load_navigation, load_posts } from "./api";
  import type { Config } from "./api/gen/models/Config";
  import { outline_id, options } from "./stores";
  import type { Options } from "./stores/options";

  let previous_options: Options | undefined;
  options.subscribe((new_options) => {
    if (previous_options) {
      for (const name of Object.keys(new_options)) {
        const previous_value = previous_options[name].value;
        const new_value = new_options[name].value;
        if (
          new_value !== undefined &&
          (previous_value === undefined || previous_value !== new_value)
        ) {
          switch (name) {
            case "show_nsfw_feeds":
              load_navigation();
              load_posts($outline_id);
              break;
          }
        }
      }
    }
    previous_options = cloneDeep(new_options);
  });

  const save_option = async (config: Config) => {
    try {
      const result = await update_config(config);
      if (result) {
        for (const [key, value] of Object.entries(config)) {
          options.set(key as keyof Options, value);
        }
      }
    } finally {
    }
  };

  const option_button_click = (name) => {
    const option = $options[name];
    if (option.type === "boolean") {
      option.value = !option.value;
      // @ts-ignore
      save_option({
        [name]: option.value,
      });
    }
  };
</script>

{#each Object.entries($options) as [name, option]}
  <li>
    <button
      type="button"
      class="dropdown-item"
      on:click|preventDefault={() => option_button_click(name)}
    >
      {#if option.type === "boolean"}
        <i
          class={`bi bi-${option.value ? "toggle-on" : "toggle-off"} text-${
            option.value ? "success" : "danger"
          }`}
        />
      {/if}
      {option.title}
    </button>
  </li>
{/each}
