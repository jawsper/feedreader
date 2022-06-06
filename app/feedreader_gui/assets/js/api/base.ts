import axios, { AxiosError } from "axios";
import Cookies from "js-cookie";

import { toasts } from "../stores";

const urls = JSON.parse(document.getElementById("urls").textContent);

export async function api_request<T>(
  path: string,
  args: any = null
): Promise<T> {
  try {
    const response = await axios.post<T>(urls[path].url, args, {
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
    });
    return response.data;
  } catch (error) {
    const axios_error = error as AxiosError;
    toasts.push({
      caption: `Error in request ${path}`,
      message: axios_error.message,
      success: false,
    });
    throw error;
  }
}
