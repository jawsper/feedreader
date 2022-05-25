import "bootstrap";

import "jquery-ui/ui/widgets/button";
import "jquery-ui/ui/widgets/dialog";

import "../css/main.scss";

import App from "./App";

new App({
  target: document.querySelector("#app"),
  hydrate: true,
});
