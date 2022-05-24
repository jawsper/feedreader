import { writable } from "svelte/store";
import { load_more_posts } from ".";

function createPosts() {
  const { subscribe, set, update } = writable([]);
  const current_id = writable(null);
  const current = writable(null);
  const loading = writable(false);
  const no_more_posts = writable(false);

  let posts_value;
  let current_post_id_value;
  let current_post_value;
  subscribe((new_value) => {
    posts_value = new_value;
  });
  current_id.subscribe((new_value) => {
    current_post_id_value = new_value;

    const post_data = posts_value.find((post) => post.id === new_value);
    current.set(post_data);
  });
  current.subscribe((new_value) => {
    current_post_value = new_value;
  });

  const append = (new_posts) => {
    update((posts) => {
      const filtered_new_posts = new_posts.filter(
        (new_post) => !posts.find((post) => post.id === new_post.id)
      );
      return [...posts, ...filtered_new_posts];
    });
  };

  const update_post = (post_id, value) => {
    update((posts) => {
      return posts.map((post) => {
        if (post.id === post_id) {
          return {
            ...post,
            ...value,
          };
        }
        return post;
      });
    });
  };

  const update_current_post = (callback) => {
    update((posts) => {
      return posts.map((post) => {
        if (post.id === current_post_id_value) return callback(post);
        return post;
      });
    });
  };

  const move_post = (direction) => {
    let current_post_idx =
      current_post_id_value !== null
        ? posts_value.findIndex((post) => post.id === current_post_id_value)
        : -1;
    if (direction > 0) {
      if (current_post_id_value === null) {
        current_id.set(posts_value[0].id);
      } else {
        const next_post = posts_value[++current_post_idx];
        if (next_post) {
          current_id.set(next_post.id);
          if (current_post_idx + 1 >= posts_value.length) {
            load_more_posts.set(true);
          }
        } else {
          load_more_posts.set(true);
        }
      }
    } else if (direction < 0) {
      if (current_post_id_value === null) return;
      const next_post = posts_value[current_post_idx - 1];
      current_id.set(next_post ? next_post.id : null);
    }
  };

  const get_current_post = () => {
    return current_post_value;
  };

  const current_open_link = () => {
    if (current_post_value) {
      window.open(current_post_value.link, "_blank", "noopener,noreferrer");
    }
  };

  return {
    subscribe,
    set,
    append,
    update_post,
    // current post funcs
    current_id: {
      subscribe: current_id.subscribe,
      set: current_id.set,
    },
    current: {
      subscribe: current.subscribe,
    },
    move_post,
    get_current_post,
    update_current_post,

    current_open_link,

    loading,
    no_more_posts,
  };
}

export const posts = createPosts();
