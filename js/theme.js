(function () {
  // Apply saved theme + language as early as possible to avoid a flash.
  var theme = null, lang = null;
  try { theme = localStorage.getItem("theme"); } catch (e) {}
  try { lang = localStorage.getItem("lang"); } catch (e) {}
  if (theme === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }
  document.documentElement.setAttribute("data-lang", lang === "de" ? "de" : "en");

  function curTheme() {
    return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
  }
  function curLang() {
    return document.documentElement.getAttribute("data-lang") === "de" ? "de" : "en";
  }

  var THEME_LABELS = {
    "light-en": "Light mode", "dark-en": "Dark mode",
    "light-de": "Heller Modus", "dark-de": "Dunkler Modus"
  };

  function updateLabels() {
    var lang = curLang();
    var tb = document.getElementById("theme-toggle");
    if (tb) {
      // Show the mode the user would switch TO (the opposite of the current one).
      var target = curTheme() === "light" ? "dark" : "light";
      tb.textContent = THEME_LABELS[target + "-" + lang];
    }
    var lb = document.getElementById("lang-toggle");
    if (lb) {
      lb.textContent = lang === "de" ? "English" : "Deutsch";
    }
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
    var lb = document.getElementById("lang-toggle");
    if (lb) {
      lb.addEventListener("click", function () {
        var next = curLang() === "de" ? "en" : "de";
        document.documentElement.setAttribute("data-lang", next);
        try { localStorage.setItem("lang", next); } catch (e) {}
        updateLabels();
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
