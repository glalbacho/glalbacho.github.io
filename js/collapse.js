(function () {
  function setup(details) {
    var summary = details.querySelector("summary");
    if (!summary) return;

    // Move everything after the summary into an animatable wrapper.
    var wrapper = document.createElement("div");
    wrapper.className = "collapse-content";
    while (summary.nextSibling) {
      wrapper.appendChild(summary.nextSibling);
    }
    details.appendChild(wrapper);

    var animating = false;

    function reflow() {
      // Force layout so the next style change animates.
      return wrapper.offsetHeight;
    }

    summary.addEventListener("click", function (e) {
      e.preventDefault();
      if (animating) return;
      animating = true;

      if (details.open) {
        // Collapse: from current height down to 0.
        wrapper.style.height = wrapper.scrollHeight + "px";
        reflow();
        wrapper.style.height = "0px";
        wrapper.addEventListener("transitionend", function done(ev) {
          if (ev.propertyName !== "height") return;
          wrapper.removeEventListener("transitionend", done);
          details.open = false;
          wrapper.style.height = "";
          animating = false;
        });
      } else {
        // Expand: render, then animate 0 -> content height.
        details.open = true;
        var target = wrapper.scrollHeight;
        wrapper.style.height = "0px";
        reflow();
        wrapper.style.height = target + "px";
        wrapper.addEventListener("transitionend", function done(ev) {
          if (ev.propertyName !== "height") return;
          wrapper.removeEventListener("transitionend", done);
          wrapper.style.height = "auto";
          animating = false;
        });
      }
    });
  }

  function init() {
    var nodes = document.querySelectorAll("details.collapse, details.abstract");
    Array.prototype.forEach.call(nodes, setup);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
