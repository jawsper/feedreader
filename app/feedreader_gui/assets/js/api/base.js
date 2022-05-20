import Cookies from "js-cookie";

import { toast } from "../stores";

const urls = JSON.parse(document.getElementById("urls").textContent);

export const api_request = (path, args, callback) => {
  let fetch_args = {
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
      toast.set({
        caption: "Error",
        message: error,
        success: false,
      });
    })
    .then(callback)
    .catch(console.log);
};
