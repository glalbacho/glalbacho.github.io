(function () {
  var IMAGES = [
    "/images/bb/IMG_0114.jpg",
    "/images/bb/IMG_0392.jpg",
    "/images/bb/IMG_0540.jpg",
    "/images/bb/IMG_0546.jpg",
    "/images/bb/IMG_0577.jpg",
    "/images/bb/IMG_0609.jpg",
    "/images/bb/IMG_0627.jpg",
    "/images/bb/IMG_0803.jpg",
    "/images/bb/IMG_0875.jpg",
    "/images/bb/IMG_0920.jpg",
    "/images/bb/IMG_0968.jpg",
    "/images/bb/IMG_1076.jpg",
    "/images/bb/IMG_1901.jpg",
    "/images/bb/IMG_1902.jpg",
    "/images/bb/IMG_1927.jpg",
    "/images/bb/IMG_1928.jpg",
    "/images/bb/IMG_1929.jpg",
    "/images/bb/IMG_1988.jpg",
    "/images/bb/IMG_2527.jpg",
    "/images/bb/IMG_2534.jpg",
    "/images/bb/IMG_2610.jpg",
    "/images/bb/IMG_2737.jpg",
    "/images/bb/IMG_2944.jpg",
    "/images/bb/IMG_3363.jpg",
    "/images/bb/IMG_4115.jpg",
    "/images/bb/IMG_7217.jpg",
    "/images/bb/IMG_8290.jpg",
    "/images/bb/IMG_8366.jpg",
    "/images/bb/IMG_8603.jpg",
    "/images/bb/IMG_9215.jpg",
    "/images/bb/IMG_9748.jpg"
  ];

  var INTERVAL = 30 * 1000; // 30 seconds

  function init() {
    var bg = document.querySelector(".hero-bg");
    if (!bg || !IMAGES.length) return;

    var layers = bg.querySelectorAll(".hero-slide");
    if (layers.length < 2) return;

    // Start at a varied position so reloads don't always show the same board.
    var order = IMAGES.slice();
    var index = 0;
    var active = 0;

    function preload(url, cb) {
      var img = new Image();
      img.onload = cb || null;
      img.src = url;
    }

    function show(i, animate) {
      var url = order[i % order.length];
      var incoming = layers[active ^ 1];
      var outgoing = layers[active];
      preload(url, function () {
        incoming.style.backgroundImage = 'url("' + url + '")';
        // Force reflow so the opacity transition runs.
        void incoming.offsetWidth;
        incoming.classList.add("is-visible");
        if (animate) outgoing.classList.remove("is-visible");
        active = active ^ 1;
      });
    }

    show(index, false);

    setInterval(function () {
      index = (index + 1) % order.length;
      show(index, true);
    }, INTERVAL);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
