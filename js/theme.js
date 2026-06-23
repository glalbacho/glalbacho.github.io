(function () {
  // Apply the saved theme as early as possible to avoid a flash.
  var saved = null;
  try {
    saved = localStorage.getItem("theme");
  } catch (e) {}
  if (saved === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }

  function label() {
    var isLight =
      document.documentElement.getAttribute("data-theme") === "light";
    return isLight ? "Dark mode" : "Light mode";
  }

  function wire() {
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.textContent = label();
    btn.addEventListener("click", function () {
      var isLight =
        document.documentElement.getAttribute("data-theme") === "light";
      if (isLight) {
        document.documentElement.removeAttribute("data-theme");
        try {
          localStorage.setItem("theme", "dark");
        } catch (e) {}
      } else {
        document.documentElement.setAttribute("data-theme", "light");
        try {
          localStorage.setItem("theme", "light");
        } catch (e) {}
      }
      btn.textContent = label();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
