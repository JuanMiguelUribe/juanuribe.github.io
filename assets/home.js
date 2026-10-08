const guideForm = document.getElementById("guide-form");
if (guideForm)
  guideForm.querySelector('button[type="submit"]').disabled = false;
if (guideForm)
  guideForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!guideForm.reportValidity()) return;
    const button = guideForm.querySelector('button[type="submit"]');
    const status = document.getElementById("form-status");
    const success = document.getElementById("form-success");
    button.disabled = true;
    button.textContent = "Enviando solicitud…";
    status.textContent = "";
    status.classList.remove("is-error");
    success.hidden = true;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch(
        "https://opal-mustang.pikapod.net/webhook/a98fab9c-ea96-489e-ad3c-a25f0faff01a",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: guideForm.elements.name.value.trim(),
            email: guideForm.elements.email.value.trim(),
            source: "landing_page",
            timestamp: new Date().toISOString(),
          }),
          mode: "no-cors",
          signal: controller.signal,
        },
      );
      if (response.type !== "opaque" && !response.ok)
        throw new Error("Request failed");
      // The current webhook returns an opaque response; email delivery cannot be confirmed.
      status.textContent =
        "Solicitud enviada. No podemos confirmar la entrega del correo; descarga tus guías aquí mismo.";
      success.hidden = false;
    } catch {
      status.classList.add("is-error");
      status.textContent =
        "No pudimos enviar tu solicitud. Inténtalo de nuevo o descarga las guías con los enlaces de esta sección.";
    } finally {
      clearTimeout(timeout);
      button.disabled = false;
      button.textContent = "Solicitar las guías";
    }
  });
