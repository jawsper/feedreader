import Cookies from "js-cookie";

import { toasts } from "../stores";
import { ApiApi, Configuration } from "./gen/";

const configuration = new Configuration({
  basePath: location.origin,
  headers: {
    "X-CSRFToken": Cookies.get("csrftoken"),
  }
})
export const api = new ApiApi(configuration);
