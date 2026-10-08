const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const base = process.env.SITE_URL || "http://127.0.0.1:8000";

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || "/usr/bin/chromium",
    headless: true,
    args: ["--no-sandbox"],
  });
  try {
    for (const width of [360, 390, 768, 1024, 1440]) {
      for (const path of ["/", "/herramientas/", "/contenido-ia/"]) {
        const page = await browser.newPage({
          viewport: { width, height: 900 },
        });
        try {
          const errors = [];
          page.on("pageerror", (error) => errors.push(error.message));
          await page.goto(base + path);
          await page.evaluate(() => document.fonts.ready);
          const result = await page.evaluate(() => ({
            overflow: document.documentElement.scrollWidth > innerWidth,
            brokenImages: [...document.images]
              .filter((image) => image.complete && image.naturalWidth === 0)
              .map((image) => image.src),
            brokenAnchors: [...document.querySelectorAll('a[href^="#"]')]
              .map((link) => link.getAttribute("href"))
              .filter(
                (href) =>
                  href.length > 1 && !document.getElementById(href.slice(1)),
              ),
          }));
          assert.deepEqual(errors, [], `${path}: JavaScript errors`);
          assert.equal(
            result.overflow,
            false,
            `${path}: overflow at ${width}px`,
          );
          assert.deepEqual(
            result.brokenImages,
            [],
            `${path}: broken loaded images`,
          );
          assert.deepEqual(result.brokenAnchors, [], `${path}: broken anchors`);
          if (width < 768) {
            const button = page.getByRole("button", { name: "Abrir menú" });
            await button.click();
            assert.equal(await button.getAttribute("aria-expanded"), "true");
            await page.keyboard.press("Escape");
            assert.equal(await button.getAttribute("aria-expanded"), "false");
            assert.equal(
              await button.evaluate(
                (element) => element === document.activeElement,
              ),
              true,
            );
          }
          console.log(`PASS ${path} at ${width}px`);
        } finally {
          await page.close();
        }
      }
    }

    const page = await browser.newPage();
    let requests = 0;
    await page.route("**/webhook/**", (route) => {
      requests++;
      return route.abort("failed");
    });
    await page.goto(base);
    await page.locator(".form-container summary").click();
    const submit = page.locator(".form-submit");
    await submit.click();
    assert.equal(requests, 0, "Required fields prevent sending");
    await page.locator("#fname").fill("Prueba");
    await page.locator("#femail").fill("correo-invalido");
    await submit.click();
    assert.equal(requests, 0, "Invalid email prevents sending");
    await page.locator("#femail").fill("test@example.invalid");
    await submit.click();
    await page.waitForFunction(() =>
      document.getElementById("form-status").textContent.includes("No pudimos"),
    );
    assert.equal(await page.locator("#form-success").isVisible(), false);
    assert.equal(await submit.isEnabled(), true);
    await page.unroute("**/webhook/**");
    await page.route("**/webhook/**", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 300));
      await route.fulfill({ status: 200, body: "ok" });
    });
    await submit.click();
    assert.equal(
      await submit.isDisabled(),
      true,
      "Loading state prevents duplicate submissions",
    );
    await page.waitForFunction(
      () => !document.getElementById("form-success").hidden,
    );
    assert.match(
      await page.locator("#form-status").textContent(),
      /No podemos confirmar/,
    );
    assert.equal(await submit.isEnabled(), true);
    console.log(
      "PASS form validation, network error, retry, loading and opaque response",
    );
    await page.close();

    const noScript = await browser.newContext({ javaScriptEnabled: false });
    const staticPage = await noScript.newPage();
    await staticPage.goto(base);
    assert.equal(await staticPage.locator("#portfolio h2").isVisible(), true);
    assert.equal(
      await staticPage.locator("#guides .guide-card a").first().isVisible(),
      true,
    );
    assert.equal(await staticPage.locator(".form-submit").isDisabled(), true);
    await noScript.close();
    const reducedMotion = await browser.newContext({ reducedMotion: "reduce" });
    const reducedPage = await reducedMotion.newPage();
    await reducedPage.goto(base);
    assert.equal(await reducedPage.locator(".reveal-ready").count(), 0);
    await reducedMotion.close();
    console.log("PASS content without JavaScript and reduced motion");
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
