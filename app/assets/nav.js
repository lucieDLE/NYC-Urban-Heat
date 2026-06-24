function bindNav() {
    const scroller = document.getElementById("scroller");
    if (!scroller || scroller.dataset.bound) return;   // run once
    scroller.dataset.bound = "1";

    const links = [...document.querySelectorAll(".nav a")];

    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          const id = e.target.id;                       // e.g. "maps"
          links.forEach((a) =>
            a.classList.toggle("on", a.getAttribute("href") === "#" + id)
          );
        }
      });
    }, { root: scroller, rootMargin: "-50% 0px -50% 0px", threshold: 0 });

    scroller.querySelectorAll("section").forEach((s) => io.observe(s));
  }

  // Dash builds the page asynchronously, so wait until #scroller exists.
  const timer = setInterval(() => {
    if (document.getElementById("scroller")) { bindNav(); clearInterval(timer); }
  }, 150);