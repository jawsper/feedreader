import $ from "jquery";
import "jquery-ui/ui/widgets/button";
import "jquery-ui/ui/widgets/dialog";
import { debounce } from "lodash";

import "../css/main.scss";

// import App from "./App";
import Navigation from "./Navigation";
import OutlineHeader from "./OutlineHeader";
import Posts from "./Posts";
import Toast from "./Toast";
import Sidebar from "./Sidebar";

import { api_request } from "./api";

import {
  outline as outline_store,
  posts as posts_store,
  load_more_posts as load_more_posts_store,
  toast as toast_store,
  outlines as outlines_store,
} from "./stores";

// const app = new App({
//   target: document.querySelector("#app")
// })

const navigation = new Navigation({
  target: document.querySelector("#outlines"),
  hydrate: true,
});

const outline_header = new OutlineHeader({
  target: document.querySelector(".content_header"),
  hydrate: true,
});

const posts_component = new Posts({
  target: document.querySelector("#content"),
  hydrate: true,
});

const toast_component = new Toast({
  target: document.querySelector("#toast"),
  hydrate: true,
});

new Sidebar({
  target: document.querySelector("#sidebar"),
  hydrate: true,
});

navigation.$on("outline", (outline_id) => {
  console.log("on outline", outline_id);
});

load_more_posts_store.subscribe((more) => {
  if (more) {
    load_more_posts(g_outline_id, null, null);
    load_more_posts_store.set(false);
  }
});

posts_component.$on("starred", (e) => {
  const { id, value } = e.detail;
  console.log("starred", e.detail);
  set_post_attr_state(id, "starred", value);
});
posts_component.$on("read", (e) => {
  const { id, value } = e.detail;
  console.log("read", e.detail);
  set_post_attr_state(id, "read", value);
});

posts_component.$on("load_more_posts", () => {
  load_more_posts(g_outline_id, null, null);
});

/*
	File: main.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

function add_new_feed(url) {
  api_request("feed_add", { url: url }, function (result) {
    if (result.success) {
      location.reload();
    }
  });
}

var outline_regex = /^outline-(\d+)$/;

$(function () {
  $("input:submit, button, a.button").button();
});

var get_unread_counts = debounce(
  function (outline_id) {
    api_request("get_unread", { outline_id: outline_id }, function (data) {
      document.title =
        data.total > 0 ? `Feedreader (${data.total})` : "Feedreader";
      if (!data.counts) return;
      for (const [outline_id, unread_count] of Object.entries(data.counts)) {
        set_unread_count(outline_id, unread_count);
      }
      set_outline_unread_count(data.counts["" + outline_id]);
    });
  },
  500,
  { trailing: true }
);

function set_unread_count(outline_id, unread_count) {
  var outline = $("#outline-" + outline_id);
  // TODO: make this in svelte
  // console.log(navigation.navigation);
  outline.toggleClass("has-unread", unread_count > 0);
  $("> .outline-line > .outline-unread-count", outline).text(unread_count);
}

function url_change(url) {
  var m = url.match(/\/outline\/(\d+)\//);
  if (m) {
    set_outline(m[1]);
  }
}

function on_popstate(e) {
  url_change(location.pathname);
}

$(function () {
  // make sure to not propagate when clicked to prevent folders from opening/closing
  //$( '#outlines a' ).click( function(e) { e.stopPropagation(); } );

  $("#outlines")
    .on(
      {
        click: function (e) {
          history.pushState(null, null, this.href);
          url_change(this.href);
          e.preventDefault();
          e.stopPropagation();
        },
      },
      "a"
    )
    .on(
      {
        click: function () {
          var outline = $(this).parent();
          var outline_id = outline.attr("id").match(outline_regex)[1];
          outline.toggleClass("folder-closed");
          set_outline_param(
            outline_id,
            "folder_opened",
            outline.hasClass("folder-closed") ? 0 : 1,
            true
          );
        },
      },
      ".folder > .outline-line"
    );

  $("#new-feed-popup").dialog({
    autoOpen: false,
    modal: true,
    buttons: {
      "Add feed": function () {
        add_new_feed($("#new-feed-url").val());
      },
      Cancel: function () {
        $(this).dialog("close");
      },
    },
    close: function () {
      $("#new-feed-url").val("");
    },
  });

  $("#button-new-feed").on("click", function () {
    $("#new-feed-popup").dialog("open");
  });
  // make the refresh button work
  $("#button_refresh_page")
    .on("click", function (e) {
      e.preventDefault();
      //get_unread_counts();
      load_navigation();
    })
    .button("option", "icons", { primary: "ui-icon-refresh" });

  // trigger initial hash change, and set window.hashchange event
  //on_hash_change();
  //$( window ).on( 'hashchange', on_hash_change );

  // if is outline url, then set the outline

  //url_change( location.pathname );
  window.addEventListener("popstate", on_popstate);

  load_navigation();

  url_change(location.pathname);
});

function load_navigation() {
  $("#button_refresh_page").button("option", "disabled", true);
  api_request("outline_get_all_outlines", {}, function (data) {
    render_navigation(data.outlines);
    $("#button_refresh_page").button("option", "disabled", false);
  });
}

function render_navigation(new_navigation) {
  outlines_store.set(new_navigation);
}

/*
	File: outline.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

/* globals */
var g_outline_id = null;
var g_outline_data = null;
var g_limit = 10;

/* directly after load init everything */

$(function () {
  $("body").on("keypress", function (e) {
    var key = e.key.toLowerCase();
    if (e.shiftKey) key = "shift+" + key;
    if (e.metaKey) key = "meta+" + key;
    if (e.ctrlKey) key = "ctrl+" + key;
    if (e.altKey) key = "alt+" + key;
    switch (key) {
      case "r":
        $("#button_refresh").trigger("click");
        break;
      case "j":
        posts_store.move_post(+1);
        break;
      case "k":
        posts_store.move_post(-1);
        break;
      case "f":
        $("body").toggleClass("fullscreen");
        if ($("body").hasClass("fullscreen")) $("#content").trigger("focus");
        break;
      case "m":
        posts_store.update_current_post((post) => {
          set_post_attr_state(post.id, "read", !post.read);
          return {
            ...post,
            read: !post.read,
          };
        });
        break;
      case "s":
        posts_store.update_current_post((post) => {
          set_post_attr_state(post.id, "starred", !post.starred);
          return {
            ...post,
            starred: !post.starred,
          };
        });
        break;
      case "v":
        posts_store.current_open_link();
        break;
      default:
        return true; // don't care
    }
    //e.preventDefault();
  });
  $("#button_refresh").on("click", function () {
    load_outline(g_outline_id, true);
  });
  $("#button_mark_all_as_read").on("click", function () {
    mark_all_as_read(g_outline_id);
  });
  $("#button_show_only_new").on("click", function () {
    set_outline_param(g_outline_id, "show_only_new");
  });
  $("#button_sort_order").on("click", function () {
    set_outline_param(g_outline_id, "sort_order");
  });
  $("#button_toggle_fullscreen").on("click", function () {
    $("body").toggleClass("fullscreen");
    if ($("body").hasClass("fullscreen")) $("#content").trigger("focus");
  });
  $("#button_prev_post").on("click", function () {
    posts_store.move_post(-1);
  });
  $("#button_next_post").on("click", function () {
    posts_store.move_post(+1);
  });
});

/* outline functions */

function set_outline(a_outline_id) {
  g_outline_id = a_outline_id;
  load_outline(g_outline_id, false);
}

function set_outline_param(a_outline_id, key, value, no_load) {
  if (!a_outline_id) return;
  let data = { outline: a_outline_id, action: key };
  if (value) data["value"] = value;

  api_request("outline_set", data, function (data) {
    if (data.success) {
      if (!no_load) load_outline(a_outline_id, true);
    }
  });
}

function set_outline_data(a_outline_id, data) {
  outline_store.set({
    id: a_outline_id,
    ...data,
  });
  g_outline_data = data;
  get_unread_counts(a_outline_id);
}

function set_outline_unread_count(count) {
  outline_store.update(($outline) => ({
    ...$outline,
    unread_count: count,
  }));
}

function count_visible_unread_posts() {
  // get all unchecked posts and skip those
  // or just all posts
  var count = $(
    g_outline_data.show_only_new
      ? "#posts .post .action.read:not(:checked)"
      : "#posts .post"
  ).length;
  return count;
}

var load_outline = debounce(
  function (a_outline_id, forced_refresh) {
    if (!a_outline_id) return;

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    api_request(
      "get_posts",
      { limit: g_limit, outline: a_outline_id, forced_refresh: forced_refresh },
      function (data) {
        if (data.success) {
          if (g_outline_id != a_outline_id) return; // attempt to prevent slow loads from overwriting the current outline
          set_outline_data(a_outline_id, data);

          $("#content").scrollTop(0);
          posts_store.current_id.set(null);
          if (data.posts.length > 0) {
            posts_store.set(data.posts);
            posts_store.no_more_posts.set(false);
          } else {
            posts_store.no_more_posts.set(true);
          }
          posts_store.loading.set(false);
        }
      }
    );
  },
  500,
  { leading: true }
);

function mark_all_as_read(a_outline_id) {
  if (!a_outline_id) return;
  api_request("outline_mark_read", { outline: a_outline_id }, function (data) {
    if (!data.error) load_outline(a_outline_id, true);
  });
}

const load_more_posts = debounce(
  function (a_outline_id, on_success, on_failure) {
    if (!a_outline_id) return;

    posts_store.loading.set(true);
    posts_store.no_more_posts.set(false);

    let skip = count_visible_unread_posts();

    api_request(
      "get_posts",
      { outline: a_outline_id, skip: skip, limit: g_limit },
      function (data) {
        if (!data.error) {
          if (data.posts.length > 0) {
            posts_store.append(data.posts);
            posts_store.no_more_posts.set(false);
            if (on_success) on_success();
          } else {
            posts_store.no_more_posts.set(true);
            if (on_failure) on_failure();
          }
          posts_store.loading.set(false);
        }
      }
    );
  },
  500,
  { leading: true }
);

/* post functions */

function set_post_attr_state(post_id, attr, state) {
  api_request(
    "post_action",
    { post: post_id, action: attr, state: state },
    function (data) {
      toast_store.set(data);
      if (data.success) get_unread_counts(g_outline_id);
    }
  );
}
