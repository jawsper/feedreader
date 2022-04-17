import $ from "jquery";
import "jquery-ui/ui/widgets/button";
import "jquery-ui/ui/widgets/dialog";
import _ from "lodash";
import Cookies from "js-cookie";

import "../css/main.scss";

/*
	File: main.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

const urls = JSON.parse(document.getElementById("urls").textContent);

function api_request(path, args, callback) {
  var fetch_args = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
    credentials: "include",
  };
  if (args) {
    fetch_args["body"] = JSON.stringify(args);
  }
  fetch(urls[path].url, fetch_args)
    .then((response) => response.json())
    .catch((error) => {
      show_result({
        caption: "Error",
        message: error,
        success: false,
      });
    })
    .then(callback)
    .catch(console.log);
}

function get_media_url(path) {
  return document.body.dataset.mediaUrl + path;
}

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

function show_result(data) {
  $("#result_text").text(data.message);
  if (data.caption) $("#result_caption_text").text(data.caption);
  $("#result_caption").toggle(data.caption ? true : false);
  $("#result_container")
    .toggleClass("ui-state-error", !data.success)
    .toggleClass("ui-state-highlight", data.success);
  $("#result_icon")
    .toggleClass("ui-icon-alert", !data.success)
    .toggleClass("ui-icon-info", data.success);
  $("#result").stop(true, true).fadeIn().delay(5000).fadeOut();
}

var get_unread_counts = _.debounce(
  function (outline_id) {
    api_request("get_unread", { outline_id: outline_id }, function (data) {
      document.title =
        data.total > 0 ? "Feedreader (" + data.total + ")" : "Feedreader";
      if (!data.counts) return;
      $.each(data.counts, set_unread_count);
      set_outline_unread_count(data.counts["" + outline_id]);
    });
  },
  500,
  { trailing: true }
);

function set_unread_count(outline_id, unread_count) {
  var outline = $("#outline-" + outline_id);
  outline.toggleClass("has-unread", unread_count > 0);
  var outline_obj = outline.data("outline");
  if (outline_obj) {
    outline_obj.unread_count = unread_count;
    outline.data("outline", outline_obj);
  }
  $("> .outline-line > .outline-unread-count", outline).text(unread_count);
}

var options = {
  show_only_unread: {
    title: "Show only unread posts",
    type: "boolean",
    default: false,
    callback: function () {
      $("#outlines").toggleClass("show-only-unread", this["value"]);
    },
  },
  show_nsfw_feeds: {
    title: "Show NSFW feeds",
    type: "boolean",
    default: false,
    callback: () => {
      load_navigation();
      $("#button_refresh").click();
    },
  },
};

function load_options() {
  var opts = [];
  $.each(options, function (k) {
    opts.push(k);
  });
  api_request("get_option", { keys: opts }, function (result) {
    $.each(options, function (name, data) {
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
        $(`#btn-option-${name}`).button("option", "icons", { primary: icon });
      }
      if (data.callback) data.callback.apply(data);
    });
  });
}

function option_button_click(name) {
  const btn = $(this);
  if (options[name].type == "boolean") {
    const new_value = !options[name].value;
    save_option(name, new_value);
    const icon = new_value ? "ui-icon-circle-check" : "ui-icon-circle-close";
    btn.button("option", "icons", { primary: icon });
  }
}

function save_option(name, value) {
  var data = {};
  data[name] = value;
  api_request("set_option", data, function (result) {
    if (result.success) {
      load_options();
    }
  });
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

  // make a button for all options
  $.each(options, function (name, option) {
    var button = $("<a>")
      .attr("id", `btn-option-${name}`)
      .on("click", function () {
        option_button_click.bind(this)(name);
      })
      .button({
        icons: { primary: "ui-icon-circle-check" },
        label: option.title,
      });
    $("#navigation .options ul").append($("<li>").append(button));
  });
  // load the options
  load_options();

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
  // make the options and refresh button work
  $("#button-options")
    .on("click", function () {
      const self = $(this);
      $("#navigation .options").toggle({
        effect: "slide",
        direction: "up",
        complete: function (args) {
          const visible = $(this).is(":visible");
          self.button("option", "icons", {
            primary: visible ? "ui-icon-carat-1-s" : "ui-icon-carat-1-e",
          });
        },
      });
    })
    .button("option", "icons", { primary: "ui-icon-carat-1-e" });
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

function get_template(id) {
  var re_template_keys = /\$\{(?:([a-z]+)\.)*([a-z_]+)\}/g;
  //var re_keyname = /^\$\{(?:([a-z]+)\.)*([a-z_]+)\}$/;

  var template = $(id).text();

  var match = false;
  var keys = {};
  while (
    (match = re_template_keys.exec(template, re_template_keys.lastIndex)) !=
    null
  ) {
    var key_name = match[0];
    keys[key_name] = match.splice(1);
  }

  /*var matched = template.match( re_template_keys );
	var keys = {};
	$.each( matched, function( k, v )
	{
		var split_key = v.match( re_keyname );
		if( !split_key )
		{
			console.debug( v );
		}
		else
		{
			var key_name = split_key[0];
			keys[ key_name ] = split_key.splice( 1 );
		}
	});*/

  return { str: template, keys: keys };
}

function apply_template(template, data_name, data) {
  var str = template.str;
  $.each(data, function (k, v) {
    var name = data_name + "." + k;
    var rx = RegExp("\\$\\{" + name + "\\}", "g");
    str = str.replace(rx, v);
  });
  return str;
}

function make_outline(template, outline) {
  var html = $(apply_template(template, "outline", outline));
  html.data("outline", outline);
  html.addClass(outline.feed_id ? "feed" : "folder");
  if (!outline.folder_opened) {
    html.addClass("folder-closed");
  }
  html.toggleClass("has-unread", outline.unread_count > 0);
  if (outline.icon) {
    $("> .outline-line", html).css(
      "background-image",
      `url(${get_media_url(outline.icon)})`
    );
  }
  return html;
}

function render_navigation(navigation) {
  var template = get_template("#templateNavigationItem");

  var main_ul = $("#outlines");
  main_ul.empty();
  $.each(navigation, function (k, outline) {
    if (!outline) return;
    var outline_html = make_outline(template, outline);

    if (outline.children && outline.children.length > 0) {
      var children = $("<ul>");
      $.each(outline.children, function (k, child) {
        if (!child) return;
        var child = make_outline(template, child);
        children.append(child);
      });
      outline_html.append(children);
    }
    main_ul.append(outline_html);
  });
}

String.prototype.format = function () {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function (match, number) {
    return typeof args[number] != "undefined" ? args[number] : match;
  });
};

/*
	File: outline.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

/* globals */
var g_outline_id = null;
var g_outline_data = null;
var g_current_post = null;
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
        move_post(+1);
        break;
      case "k":
        move_post(-1);
        break;
      case "f":
        $("body").toggleClass("fullscreen");
        if ($("body").hasClass("fullscreen")) $("#content").trigger("focus");
        break;
      case "m":
        if (g_current_post != null) {
          var cb = g_current_post.find(".footer .action.read");
          cb.prop("checked", !cb.prop("checked"));
          set_post_read_state(
            post_get_id(g_current_post),
            cb.is(":checked") ? 1 : 0
          );
        }
        break;
      case "s":
        if (g_current_post != null) {
          var cb = g_current_post.find(".footer .action.starred");
          cb.prop("checked", !cb.prop("checked"));
          set_post_starred_state(
            post_get_id(g_current_post),
            cb.is(":checked") ? 1 : 0
          );
        }
        break;
      case "v":
        if (g_current_post != null) {
          window.open(g_current_post.find(".link a").attr("href"), "_blank");
        }
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
    move_post(-1);
  });
  $("#button_next_post").on("click", function () {
    move_post(+1);
  });
  $("#load_more_posts a").on("click", function () {
    load_more_posts(g_outline_id, null, null);
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
  g_outline_data = data;
  $("#outline_title > a").text(data.title).attr("href", data.html_url);
  update_outline_unread_count();
  $("#button_sort_order").button(
    "option",
    "label",
    data.sort_order == "ASC" ? "Oldest first" : "Newest first"
  );

  get_unread_counts(a_outline_id);
}

function set_outline_unread_count(count) {
  g_outline_data.unread_count = count;
  update_outline_unread_count();
}
function update_outline_unread_count() {
  $("#button_show_only_new").button(
    "option",
    "label",
    g_outline_data.show_only_new
      ? g_outline_data.unread_count +
          " new item" +
          (g_outline_data.unread_count != 1 ? "s" : "")
      : "All items"
  );
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

var load_outline = _.debounce(
  function (a_outline_id, forced_refresh) {
    if (!a_outline_id) return;

    $("#load_more_posts").hide();
    $("#no_more_posts").hide();

    api_request(
      "get_posts",
      { limit: g_limit, outline: a_outline_id, forced_refresh: forced_refresh },
      function (data) {
        if (data.success) {
          if (g_outline_id != a_outline_id) return; // attempt to prevent slow loads from overwriting the current outline
          set_outline_data(a_outline_id, data);

          $("#content").scrollTop(0);
          $("#posts").empty();
          g_current_post = null;
          if (data.posts.length > 0) {
            $.each(data.posts, function (k, post) {
              $("#posts").append(post_build_html(post, data.is_feed));
              post_attach_handlers(post.id);
            });
            $("#no_more_posts").hide();
          } else {
            $("#no_more_posts").show();
          }
          $("#load_more_posts").show();
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

var load_more_posts = _.debounce(
  function (a_outline_id, on_success, on_failure) {
    if (!a_outline_id) return;

    $("#load_more_posts").hide();
    $("#no_more_posts").hide();

    let skip = count_visible_unread_posts();

    api_request(
      "get_posts",
      { outline: a_outline_id, skip: skip, limit: g_limit },
      function (data) {
        if (!data.error) {
          if (data.posts.length > 0) {
            $.each(data.posts, function (k, post) {
              if (id_get_post(post.id).length == 0) {
                $("#posts").append(post_build_html(post, data.is_feed));
                post_attach_handlers(post.id);
              }
            });
            $("#no_more_posts").hide();
            if (on_success) on_success();
          } else {
            $("#no_more_posts").show();
            if (on_failure) on_failure();
          }
          $("#load_more_posts").show();
        }
      }
    );
  },
  500,
  { leading: true }
);

/* post functions */

function post_get_id(post) {
  return post && post.attr("id").replace(/[^\d]/g, "");
}
function id_get_post(post_id) {
  return $("#post_" + post_id);
}

function set_post_read_state(post_id, state) {
  set_post_attr_state(post_id, "read", state);
  if (!state) {
    var post = id_get_post(post_id);
    post.data("do-not-auto-mark-read", true);
  }
  // only visually update the unread count.
  // TODO: every now and then actually do API hit...?
  // Maybe better on a timer...
  // outline_change_unread_count(g_outline_id, state ? -1 : 1);
  // g_outline_data.unread_count += state ? -1 : 1;

  // update_outline_unread_count();
}
function set_post_starred_state(post_id, state) {
  set_post_attr_state(post_id, "starred", state);
}
function set_post_attr_state(post_id, attr, state) {
  api_request(
    "post_action",
    { post: post_id, action: attr, state: state },
    function (data) {
      show_result(data);
      if (data.success) get_unread_counts(g_outline_id);
    }
  );
}

function select_post_by_id(post_id) {
  select_post(id_get_post(post_id));
}

function select_post(post) {
  if (
    g_current_post != null &&
    post.length > 0 &&
    g_current_post.attr("id") == post.attr("id")
  )
    return;

  if (g_current_post != null) g_current_post.removeClass("current");
  if (post.length == 0) {
    g_current_post = null;
    return;
  }
  g_current_post = post;
  g_current_post.addClass("current");

  post[0].scrollIntoView(true);

  if (
    !post.data("do-not-auto-mark-read") &&
    !post.find(".footer .action.read").attr("checked")
  ) {
    post.find(".footer .action.read").attr("checked", true);
    set_post_read_state(post_get_id(post), 1);
  }
}

function post_attach_handlers(post_id) {
  id_get_post(post_id)
    .on("mouseup", function () {
      select_post_by_id(post_id);
    })
    .find(".footer .action.starred")
    .on("click", function () {
      set_post_starred_state(post_id, $(this).is(":checked") ? 1 : 0);
    })
    .end()
    .find(".footer .action.read")
    .on("click", function () {
      set_post_read_state(post_id, $(this).is(":checked") ? 1 : 0);
    })
    .end()
    .find(".body .content a")
    .attr("target", "_blank");
}

function post_build_html(post, is_feed) {
  var postTemplate = $("#postTemplate").html();
  var template = postTemplate.format(
    post.id,
    post.link,
    post.title,
    post.pubDate,
    (is_feed ? "" : "from " + post.feedTitle + " ") +
      (post.author
        ? 'by <span class="authorName">{0}</span>'.format(post.author)
        : ""),
    post.content,
    post.starred ? ' checked="checked"' : "",
    post.read ? ' checked="checked"' : ""
  );
  return template;
}

function move_post(direction) {
  if (direction > 0) {
    if (g_current_post == null) {
      select_post($("#posts .post").first());
    } else {
      var next_post = g_current_post.next(".post");
      if (next_post.length > 0) {
        select_post(next_post);
        if (g_current_post.next(".post").length == 0) {
          load_more_posts(g_outline_id, null, null);
        }
      } else {
        load_more_posts(
          g_outline_id,
          function () {
            move_post(+1);
          },
          null
        );
      }
    }
  } else {
    if (g_current_post == null) return; // can't do anything
    select_post(g_current_post.prev(".post"));
  }
}
