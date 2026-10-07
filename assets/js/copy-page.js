// js/copy-page.ts
document.querySelectorAll(".copy-page-main-btn").forEach(
  (btn) => {
    btn.addEventListener("click", () => {
      navigator?.clipboard?.writeText(globalThis.location.href).then(() => {
        const label = btn.querySelector(".copy-page-main-label");
        if (label) {
          const original = label.textContent;
          label.textContent = "Copied!";
          setTimeout(() => {
            label.textContent = original;
          }, 2e3);
        }
      }).catch(() => {
        const label = btn.querySelector(".copy-page-main-label");
        if (label) {
          const original = label.textContent;
          label.textContent = "Copy failed";
          setTimeout(() => {
            label.textContent = original;
          }, 2e3);
        }
      });
    });
  }
);
var panel = document.getElementById("copy-page-menu");
var toggleBtn = document.querySelector(
  ".copy-page-toggle-btn"
);
var supportsAnchor = CSS.supports("anchor-name", "--a");
if (!supportsAnchor && panel) {
  panel.style.setProperty("position-anchor", "unset");
  panel.style.setProperty("position-area", "unset");
  panel.style.setProperty("position-try-fallbacks", "none");
}
panel?.addEventListener("toggle", (event) => {
  const e = event;
  const chevron = toggleBtn?.querySelector(".copy-page-chevron");
  const splitBtn = toggleBtn?.closest(".copy-page-split");
  if (e.newState === "open" && splitBtn && toggleBtn) {
    if (!supportsAnchor) {
      requestAnimationFrame(() => {
        const btnRect = toggleBtn.getBoundingClientRect();
        const splitRect = splitBtn.getBoundingClientRect();
        const panelWidth = panel.offsetWidth;
        const top = btnRect.bottom + 4;
        let right = globalThis.innerWidth - splitRect.right;
        const left = globalThis.innerWidth - right - panelWidth;
        if (left < 8) {
          right = globalThis.innerWidth - panelWidth - 8;
        }
        panel.style.top = `${top}px`;
        panel.style.right = `${right}px`;
      });
    }
  }
  if (chevron) {
    chevron.style.transform = e.newState === "open" ? "rotate(180deg)" : "";
  }
});
