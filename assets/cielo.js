// Small pointer response on the illustrated home composition. Reading never depends on motion.
(() => {
  const hero = document.querySelector(".home-hero");
  const scene = document.querySelector(".hero-playground");
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  if (
    !hero ||
    !scene ||
    !matchMedia("(hover: hover) and (pointer: fine)").matches
  )
    return;
  let frame;
  hero.addEventListener("pointermove", (event) => {
    if (motion.matches) return;
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      const rect = hero.getBoundingClientRect();
      scene.style.setProperty(
        "--play-x",
        `${((event.clientX - rect.left) / rect.width - 0.5) * 12}px`,
      );
      scene.style.setProperty(
        "--play-y",
        `${((event.clientY - rect.top) / rect.height - 0.5) * 9}px`,
      );
    });
  });
  const reset = () => {
    cancelAnimationFrame(frame);
    scene.style.removeProperty("--play-x");
    scene.style.removeProperty("--play-y");
  };
  hero.addEventListener("pointerleave", reset);
  motion.addEventListener("change", reset);
})();
