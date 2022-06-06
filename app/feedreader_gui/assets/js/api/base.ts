import Cookies from "js-cookie";

import { toasts } from "../stores";

const urls = JSON.parse(document.getElementById("urls").textContent);

export async function api_request<T>(path: string, args: any = null): Promise<T> {
  let fetch_args: RequestInit = {
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
  try {
    const response = await fetch(urls[path].url, fetch_args);
    return response.json();
  } catch (error) {
    toasts.push({
      caption: "Error",
      message: error,
      success: false,
    });
    throw error;
  }
};
