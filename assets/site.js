// Progressive enhancement: content remains readable without JavaScript.
const menuButton = document.querySelector(".menu-toggle");
const mobileMenu = document.getElementById("mobile-menu");
function closeMenu() {
  if (!menuButton || !mobileMenu) return;
  menuButton.setAttribute("aria-expanded", "false");
  mobileMenu.hidden = true;
  mobileMenu.classList.remove("open");
}
if (menuButton && mobileMenu) {
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") !== "true";
    menuButton.setAttribute("aria-expanded", String(open));
    mobileMenu.hidden = !open;
    mobileMenu.classList.toggle("open", open);
  });
  mobileMenu
    .querySelectorAll("a")
    .forEach((link) => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      menuButton.getAttribute("aria-expanded") === "true"
    ) {
      closeMenu();
      menuButton.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (
      !mobileMenu.contains(event.target) &&
      !menuButton.contains(event.target)
    )
      closeMenu();
  });
  matchMedia("(min-width: 768px)").addEventListener("change", (event) => {
    if (event.matches) closeMenu();
  });
}
if (
  !matchMedia("(prefers-reduced-motion: reduce)").matches &&
  "IntersectionObserver" in window
) {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries)
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
    },
    { threshold: 0.08 },
  );
  document
    .querySelectorAll("main .fade-in, main .fade-up")
    .forEach((element) => {
      // Do not delay the first impression or hide content already in view.
      if (element.getBoundingClientRect().top > innerHeight)
        element.classList.add("reveal-ready");
      observer.observe(element);
    });
}
