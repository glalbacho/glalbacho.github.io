(function () {
  // Apply saved theme + language as early as possible to avoid a flash.
  var theme = null, lang = null;
  try { theme = localStorage.getItem("theme"); } catch (e) {}
  try { lang = localStorage.getItem("lang"); } catch (e) {}
  if (theme === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }
  document.documentElement.setAttribute("data-lang", (lang === "de" || lang === "ku") ? lang : "en");

  function curTheme() {
    return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
  }
  function curLang() {
    var l = document.documentElement.getAttribute("data-lang");
    return (l === "de" || l === "ku") ? l : "en";
  }

  var THEME_LABELS = {
    "light-en": "Light mode", "dark-en": "Dark mode",
    "light-de": "Heller Modus", "dark-de": "Dunkler Modus",
    "light-ku": "Moda ronî", "dark-ku": "Moda tarî"
  };

  function updateLabels() {
    var lang = curLang();
    var tb = document.getElementById("theme-toggle");
    if (tb) {
      var target = curTheme() === "light" ? "dark" : "light";
      var txt = tb.querySelector(".btn-text") || tb;
      txt.textContent = THEME_LABELS[target + "-" + lang];
    }
    var opts = document.querySelectorAll(".lang-option");
    for (var i = 0; i < opts.length; i++) {
      var on = opts[i].getAttribute("data-set-lang") === lang;
      opts[i].classList.toggle("active", on);
    }
  }

  function setLang(next) {
    document.documentElement.setAttribute("data-lang", next);
    try { localStorage.setItem("lang", next); } catch (e) {}
    updateLabels();
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
        updateLabels();
      });
    }

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
      var opts = menu.querySelectorAll(".lang-option");
      for (var i = 0; i < opts.length; i++) {
        opts[i].addEventListener("click", function () {
          setLang(this.getAttribute("data-set-lang"));
          close();
        });
      }
      // Close when clicking elsewhere or pressing Escape.
      document.addEventListener("click", function (e) {
        if (!menu.contains(e.target)) close();
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") close();
      });
    }

    updateLabels();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
