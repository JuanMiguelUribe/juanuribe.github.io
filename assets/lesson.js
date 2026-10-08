for (const button of document.querySelectorAll("[data-copy]")) {
  button.hidden = false;
  button.addEventListener("click", async () => {
    const text = document.getElementById(button.dataset.copy).textContent;
    const status = button.parentElement.querySelector(".copy-status");
    try {
      if (!navigator.clipboard?.writeText)
        throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(text);
      status.textContent =
        "Estructura copiada. Rellena los campos con tu contexto.";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(document.getElementById(button.dataset.copy));
      const selection = getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent =
        "Seleccionamos la estructura. Puedes copiarla con el menú de tu navegador.";
    }
  });
}
