(function () {
  // Apply saved theme as early as possible to avoid a flash.
  // Language is determined by the URL path (/, /de/, /ku/), not by JS.
  var theme = null;
  try { theme = localStorage.getItem("theme"); } catch (e) {}
  if (theme === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }

  function curTheme() {
    return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function updateThemeLabel() {
    var tb = document.getElementById("theme-toggle");
    if (!tb) return;
    // Show the label for the mode the button switches TO.
    var next = curTheme() === "light" ? "dark" : "light";
    var label = tb.getAttribute(next === "light" ? "data-label-light" : "data-label-dark");
    var txt = tb.querySelector(".btn-text") || tb;
    if (label) txt.textContent = label;
  }

  function wire() {
    var tb = document.getElementById("theme-toggle");
    if (tb) {
      tb.addEventListener("click", function () {
        if (curTheme() === "light") {
          document.documentElement.removeAttribute("data-theme");
          try { localStorage.setItem("theme", "dark"); } catch (e) {}
        } else {
          document.documentElement.setAttribute("data-theme", "light");
          try { localStorage.setItem("theme", "light"); } catch (e) {}
        }
        updateThemeLabel();
      });
    }

    // Language menu: the options are plain links to the other-language URLs;
    // JS only handles opening/closing the dropdown.
    var menu = document.querySelector(".lang-menu");
    var toggle = document.getElementById("lang-toggle");
    if (menu && toggle) {
      function close() {
        menu.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
      toggle.addEventListener("click", function (e) {
        e.stopPropagation();
        var open = menu.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
      document.addEventListener("click", function (e) {
        if (!menu.contains(e.target)) close();
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") close();
      });
    }

    updateThemeLabel();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
