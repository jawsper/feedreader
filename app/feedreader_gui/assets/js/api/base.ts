import Cookies from "js-cookie";

import { toasts } from "../stores";
import { ApiApi, Configuration } from "./gen/";

const configuration = new Configuration({
  basePath: location.origin,
  headers: {
    "X-CSRFToken": Cookies.get("csrftoken"),
  },
  middleware: [
    {
      post: async (context) => {
        if (context.response.status >= 400) {
          toasts.push({
            caption: `Error in request ${context.url}`,
            message: `Status code: ${context.response.status}`,
            success: false,
          });
        }
      },
      onError: async (context) => {
        toasts.push({
          caption: `Exception on request ${context.url}`,
          message: `${context.error}`,
          success: false,
        });
      },
    },
  ],
});
export const api = new ApiApi(configuration);
