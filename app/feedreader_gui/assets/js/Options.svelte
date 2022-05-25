<script lang="ts">
  import jquery from "jquery";
  import { cloneDeep } from "lodash";
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";
  import { api_request, load_navigation, load_posts } from "./api";
  import { outline_id, options } from "./stores";
  import type { Options } from "./stores/options";

  export let visible: boolean = false;

  let previous_options: Options | undefined;
  options.subscribe((new_options) => {
    for (const name of Object.keys(new_options)) {
      const previous_value = previous_options && previous_options[name].value;
      const new_value = new_options[name].value;
      if (
        new_value !== undefined &&
        (previous_value === undefined || previous_value !== new_value)
      ) {
        switch (name) {
          case "show_only_unread":
            jquery("#outlines").toggleClass("show-only-unread", new_value);
            break;
          case "show_nsfw_feeds":
            load_navigation();
            load_posts($outline_id);
            break;
        }
      }
    }

    previous_options = cloneDeep(new_options);
  });

  onMount(() => {
    options.load();
  });

  const save_option = (name: string, value: any) => {
    const data = {
      [name]: value,
    };
    api_request("set_option", data, (result) => {
      if (result.success) {
        options.set(name as any, value);
      }
    });
  };

  const option_button_click = (name) => {
    const option = $options[name];
    if (option.type === "boolean") {
      option.value = !option.value;
      save_option(name, option.value);
    }
  };
</script>

{#if visible}
  <div class="options" transition:slide>
    <ul class="clean">
      {#each Object.entries($options) as [name, option]}
        <li>
          <button
            class="option-button ui-button ui-corner-all ui-widget"
            on:click={() => option_button_click(name)}
          >
            {#if option.type === "boolean"}
              <span
                class={`ui-button-icon ui-icon ui-icon-circle-${
                  option.value ? "check" : "close"
                }`}
              />
              <span class="ui-button-icon-space" />
            {/if}
            {option.title}
          </button>
        </li>
      {/each}
    </ul>
    <hr class="" />
  </div>
{/if}
