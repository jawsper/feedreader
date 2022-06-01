import "bootstrap";

import "../css/main.scss";

import App from "./App";

new App({
  target: document.querySelector("#app"),
  hydrate: true,
});
