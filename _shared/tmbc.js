(function () {
  document.body.classList.add("tmbc-has-sticky");
  var bar = document.querySelector(".tmbc-sticky-bar");
  if (!bar) return;
  var phone = document.body.dataset.bizPhone;
  var map = document.body.dataset.bizMap;
  var call = bar.querySelector(".tmbc-sticky-call");
  var dir = bar.querySelector(".tmbc-sticky-map");
  if (call && phone) call.href = phone;
  if (dir && map) dir.href = map;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var els = document.querySelectorAll(".reveal");
  if (!els.length || !("IntersectionObserver" in window)) {
    els.forEach(function (el) {
      el.classList.add("is-visible");
    });
    return;
  }
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("is-visible");
          io.unobserve(e.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  els.forEach(function (el) {
    io.observe(el);
  });
})();
