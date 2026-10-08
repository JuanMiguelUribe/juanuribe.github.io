const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const pages = require("../scripts/public-pages.json");
const base = process.env.SITE_URL || "http://127.0.0.1:8000";
(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  try {
    const page = await browser.newPage({
      viewport: { width: 390, height: 900 },
    });
    const errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto(base);
    await page
      .getByRole("link", { name: "Empezar a aprender", exact: true })
      .click();
    await page.locator("a.learning-route").first().click();
    assert.equal(new URL(page.url()).pathname, "/aprender/llms/");
    await page.getByRole("link", { name: "Ir al ejercicio" }).click();
    assert.equal(new URL(page.url()).hash, "#practica");
    console.log("PASS home → learning route → LLM practice");

    await page.goto(base + "/recursos/");
    assert.equal(await page.locator("[data-resource]:visible").count(), 8);
    await page
      .getByRole("button", { name: "Automatizar", exact: true })
      .click();
    assert.equal(await page.locator("[data-resource]:visible").count(), 3);
    assert.match(page.url(), /tema=automatizar/);
    await page.locator("#resource-search").fill("n8n");
    assert.equal(await page.locator("[data-resource]:visible").count(), 1);
    await page.reload();
    assert.equal(await page.locator("[data-resource]:visible").count(), 1);
    assert.equal(await page.locator("#resource-search").inputValue(), "n8n");
    await page.locator("#resource-search").fill("sin-coincidencias-123");
    assert.equal(await page.locator("#resource-empty").isVisible(), true);
    await page.getByRole("button", { name: "Ver todos los recursos" }).click();
    assert.equal(await page.locator("[data-resource]:visible").count(), 8);
    assert.equal(
      await page
        .locator("#resource-search")
        .evaluate((e) => e === document.activeElement),
      true,
    );
    await page.locator("#resource-search").fill("musica");
    assert.equal(
      await page
        .getByRole("heading", { name: "Una idea musical con IA" })
        .isVisible(),
      true,
    );
    assert.match(
      await page.locator("#resource-count").textContent(),
      /recursos disponibles/,
    );
    console.log(
      "PASS filters, accents, URL restoration, empty state and reset",
    );

    await page.addInitScript(() => {
      Object.defineProperty(navigator, "clipboard", {
        value: {
          writeText: async (text) => {
            window.copiedText = text;
          },
        },
        configurable: true,
      });
    });
    await page.goto(base + "/aprender/llms/");
    await page.getByRole("button", { name: "Copiar estructura" }).click();
    assert.match(await page.evaluate(() => window.copiedText), /Material:/);
    assert.match(await page.locator(".copy-status").textContent(), /copiada/);
    await page.evaluate(() => {
      navigator.clipboard.writeText = () => Promise.reject(new Error("denied"));
    });
    await page.getByRole("button", { name: "Copiar estructura" }).click();
    await page.waitForFunction(() =>
      document
        .querySelector(".copy-status")
        .textContent.includes("Seleccionamos"),
    );
    assert.match(
      await page.evaluate(() => getSelection().toString()),
      /Material:/,
    );
    console.log("PASS copy success and accessible selection fallback");

    const localLinks = new Set();
    const titles = new Set();
    for (const [path, metadata] of Object.entries(pages)) {
      const response = await page.goto(base + path);
      assert.equal(response.status(), 200);
      assert.equal(await page.locator("main h1").count(), 1, `One H1: ${path}`);
      const title = await page.title();
      assert.equal(titles.has(title), false, `Unique title: ${path}`);
      titles.add(title);
      assert.equal(
        await page.locator("link[rel=canonical]").getAttribute("href"),
        "https://juanuribeia.com" + path,
      );
      const links = await page
        .locator("a[href]")
        .evaluateAll((elements) => elements.map((e) => e.getAttribute("href")));
      for (const href of links) if (href.startsWith("/")) localLinks.add(href);
    }
    for (const href of localLinks) {
      const url = new URL(href, base);
      const response = await page.goto(url.href);
      assert.equal(
        (
          response ||
          (await page.request.get(url.origin + url.pathname + url.search))
        ).status(),
        200,
        `Broken internal link: ${href}`,
      );
      if (url.hash)
        assert.equal(
          await page.evaluate(
            (id) => !!document.getElementById(id),
            decodeURIComponent(url.hash.slice(1)),
          ),
          true,
          `Missing target: ${href}`,
        );
    }
    assert.deepEqual(errors, []);
    console.log(
      `PASS ${Object.keys(pages).length} pages, unique metadata and ${localLinks.size} internal destinations`,
    );
    await page.close();
    const noJS = await browser.newContext({ javaScriptEnabled: false });
    const fallback = await noJS.newPage();
    await fallback.goto(base + "/recursos/");
    assert.equal(await fallback.locator("[data-resource]:visible").count(), 8);
    assert.equal(
      await fallback.locator(".library-controls").isVisible(),
      false,
    );
    await fallback.goto(base + "/aprender/llms/");
    assert.equal(await fallback.locator("#example-prompt").isVisible(), true);
    assert.equal(await fallback.locator(".copy-prompt").isVisible(), false);
    await noJS.close();
    console.log("PASS resource library and prompt without JavaScript");
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
