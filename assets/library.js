const library = document.querySelector("[data-library]");
if (library) {
  const controls = library.querySelector(".library-controls");
  const input = library.querySelector("#resource-search");
  const filters = [...library.querySelectorAll("[data-filter]")];
  const items = [...library.querySelectorAll("[data-resource]")];
  const count = library.querySelector("#resource-count");
  const empty = library.querySelector("#resource-empty");
  const normalize = (value) =>
    value
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  const parameters = new URLSearchParams(location.search);
  let category = filters.some(
    (button) => button.dataset.filter === parameters.get("tema"),
  )
    ? parameters.get("tema")
    : "todos";
  input.value = parameters.get("q") || "";
  function render(updateURL = true) {
    const words = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const item of items) {
      const matchesTopic =
        category === "todos" ||
        item.dataset.category.split(" ").includes(category);
      const text = normalize(item.dataset.search);
      item.hidden =
        !matchesTopic || !words.every((word) => text.includes(word));
      if (!item.hidden) visible++;
    }
    for (const filter of filters)
      filter.setAttribute(
        "aria-pressed",
        String(filter.dataset.filter === category),
      );
    count.textContent = `${visible} ${visible === 1 ? "recurso disponible" : "recursos disponibles"}`;
    empty.hidden = visible > 0;
    if (updateURL) {
      const url = new URL(location.href);
      input.value.trim()
        ? url.searchParams.set("q", input.value.trim())
        : url.searchParams.delete("q");
      category !== "todos"
        ? url.searchParams.set("tema", category)
        : url.searchParams.delete("tema");
      history.replaceState(null, "", url);
    }
  }
  controls.hidden = false;
  input.addEventListener("input", () => render());
  filters.forEach((button) =>
    button.addEventListener("click", () => {
      category = button.dataset.filter;
      render();
    }),
  );
  library.querySelector("[data-reset]").addEventListener("click", () => {
    input.value = "";
    category = "todos";
    render();
    input.focus();
  });
  window.addEventListener("popstate", () => {
    const params = new URLSearchParams(location.search);
    input.value = params.get("q") || "";
    category = filters.some(
      (button) => button.dataset.filter === params.get("tema"),
    )
      ? params.get("tema")
      : "todos";
    render(false);
  });
  render(false);
}
