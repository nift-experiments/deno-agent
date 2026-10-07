import {
  __name
} from "../chunk-Y5CWL2B3.js";

// js/lint_rules.ts
var searchbar = document.getElementById("lint-rule-search");
var tagButtons = document.querySelectorAll(
  "[data-tag-btn]"
);
var activeTags = /* @__PURE__ */ new Set();
function updateVisibility() {
  const searchQuery = searchbar?.value ?? "";
  const allBoxes = document.querySelectorAll(".lint-rule-box");
  for (const box of allBoxes) {
    const matchesSearch = !searchQuery || box.id.includes(searchQuery);
    const boxTags = (box.dataset.tags ?? "").split(",").filter(Boolean);
    const matchesFilter = activeTags.size === 0 || boxTags.some((tag) => activeTags.has(tag));
    box.style.display = matchesSearch && matchesFilter ? "" : "none";
  }
}
__name(updateVisibility, "updateVisibility");
function handleTagFilterButtonClick(button) {
  const tag = button.dataset.tagBtn;
  const isActive = activeTags.has(tag);
  if (isActive) {
    activeTags.delete(tag);
    button.setAttribute("aria-pressed", "false");
  } else {
    activeTags.add(tag);
    button.setAttribute("aria-pressed", "true");
  }
  updateVisibility();
}
__name(handleTagFilterButtonClick, "handleTagFilterButtonClick");
if (searchbar) {
  searchbar.addEventListener("input", updateVisibility);
}
for (const button of tagButtons) {
  button.addEventListener("click", () => handleTagFilterButtonClick(button));
}
