import $ from "jquery";
import "jquery-ui/ui/widgets/button";
import "jquery-ui/ui/widgets/dialog";

import "../css/main.scss";

// import App from "./App";
import Navigation from "./Navigation";
import OutlineHeader from "./OutlineHeader";
import Posts from "./Posts";
import Toast from "./Toast";
import Sidebar from "./Sidebar";

import { api_request, load_more_posts } from "./api";
import { get_unread_counts } from "./api/posts";

import {
  posts as posts_store,
  load_more_posts as load_more_posts_store,
  toast as toast_store,
} from "./stores";
import { load_posts } from "./api/posts";
import { outline_id } from "./stores/outline";

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

outline_header.$on("toggle-fullscreen", () => {
  $("body").toggleClass("fullscreen");
  if ($("body").hasClass("fullscreen")) $("#content").trigger("focus");
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
    load_more_posts();
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

  window.addEventListener("popstate", on_popstate);

  url_change(location.pathname);
});

/*
	File: outline.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

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
});

/* outline functions */

function set_outline(a_outline_id) {
  outline_id.set(a_outline_id);
}

/* post functions */

const set_post_attr_state = (post_id, attr, state) => {
  api_request(
    "post_action",
    { post: post_id, action: attr, state: state },
    (data) => {
      toast_store.set(data);
      if (data.success) get_unread_counts();
    }
  );
};
