import "./utils";
import "./categs";
import "./checkState";
import "./bookmarks";
import "./sendAvaForm";

import "../css/index.css";


//  third parties
import * as bootstrap from 'bootstrap';
window.bootstrap = bootstrap;

window.htmx = require('htmx.org');

const modal = new bootstrap.Modal(document.getElementById("modal"));
  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dialog") {
      modal.show()
    }
  })
  htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
    modal.hide()
    e.detail.shouldSwap = false
  }
})
// form with errors->cancel-> open again(form + err should flush)
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
  })