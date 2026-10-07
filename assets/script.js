// fs:/_components/ThemeToggle/darkmode.js
var THEME_KEY = "denoDocsTheme";
var DARK_CLASS = "dark";
var LIGHT_CLASS = "light";
function getPreferredTheme() {
  if (THEME_KEY in localStorage) {
    return localStorage[THEME_KEY];
  }
  return globalThis.matchMedia("(prefers-color-scheme: dark)").matches ? DARK_CLASS : LIGHT_CLASS;
}
function setTheme(theme) {
  const root = document.documentElement;
  root.classList.add(theme);
  root.classList.remove(theme === DARK_CLASS ? LIGHT_CLASS : DARK_CLASS);
}
setTheme(getPreferredTheme());

// fs:/_components/ThemeToggle/darkmode-toggle.js
var THEME = {
  DARK: "dark",
  LIGHT: "light",
  STORAGE_KEY: "denoDocsTheme"
};
var colorThemes = document.querySelectorAll("[data-color-mode]");
var darkModeToggleButton = document.getElementById("theme-toggle");
var getUserPreference = () => {
  const storedTheme = localStorage.getItem(THEME.STORAGE_KEY);
  if (storedTheme) return storedTheme;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? THEME.DARK : THEME.LIGHT;
};
var setTheme2 = (theme) => {
  document.documentElement.classList.remove(THEME.DARK, THEME.LIGHT);
  document.documentElement.classList.add(theme);
  colorThemes.forEach((el) => {
    el.setAttribute("data-color-mode", theme);
  });
  localStorage.setItem(THEME.STORAGE_KEY, theme);
};
var toggleDarkMode = () => {
  const currentTheme = getUserPreference();
  const newTheme = currentTheme === THEME.LIGHT ? THEME.DARK : THEME.LIGHT;
  setTheme2(newTheme);
};
var init = () => {
  if (!darkModeToggleButton) {
    console.warn("Theme toggle button not found");
    return;
  }
  setTheme2(getUserPreference());
  darkModeToggleButton.addEventListener("click", toggleDarkMode);
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    if (!localStorage.getItem(THEME.STORAGE_KEY)) {
      setTheme2(e.matches ? THEME.DARK : THEME.LIGHT);
    }
  });
};
init();

// fs:/_components/SidebarNav/script.js
var sidebar = document.getElementById("nav");
var button = document.getElementById("hamburger-button");
if (sidebar) {
  const toggleButtons = document.querySelectorAll(
    ".sub-nav-toggle[data-accordion-toggle]"
  );
  toggleButtons.forEach((toggleButton) => {
    const accordionId = toggleButton.getAttribute("data-accordion-toggle");
    const parentLi = toggleButton.closest("li");
    const isExpanded = localStorage.getItem(`accordion-${accordionId}`) === "true";
    if (parentLi) {
      if (isExpanded) {
        parentLi.classList.add("expanded");
        toggleButton.setAttribute("aria-expanded", "true");
      } else {
        toggleButton.setAttribute("aria-expanded", "false");
      }
    }
    toggleButton.addEventListener("click", () => {
      if (parentLi) {
        parentLi.classList.add("user-interaction");
        const wasExpanded = parentLi.classList.contains("expanded");
        if (wasExpanded) {
          parentLi.classList.remove("expanded");
          toggleButton.setAttribute("aria-expanded", "false");
          localStorage.setItem(`accordion-${accordionId}`, "false");
        } else {
          toggleButtons.forEach((otherToggleButton) => {
            const otherAccordionId = otherToggleButton.getAttribute(
              "data-accordion-toggle"
            );
            const otherParentLi = otherToggleButton.closest("li");
            if (otherToggleButton !== toggleButton && otherParentLi) {
              otherParentLi.classList.remove("expanded");
              otherToggleButton.setAttribute("aria-expanded", "false");
              localStorage.setItem(`accordion-${otherAccordionId}`, "false");
            }
          });
          parentLi.classList.add("expanded");
          toggleButton.setAttribute("aria-expanded", "true");
          localStorage.setItem(`accordion-${accordionId}`, "true");
        }
      }
    });
  });
}
if (sidebar) {
  sidebar.querySelectorAll("[data-disclosure]").forEach((group) => {
    const list = group.querySelector(":scope > ul");
    const buttons = group.querySelectorAll("[data-disclosure-toggle]");
    if (!list) return;
    const storageKey = `sidebar-open:${list.id}`;
    const setOpen = (open, persist) => {
      group.setAttribute("data-open", String(open));
      list.hidden = !open;
      buttons.forEach((b) => b.setAttribute("aria-expanded", String(open)));
      if (persist) localStorage.setItem(storageKey, String(open));
    };
    if (group.getAttribute("data-open") !== "true" && localStorage.getItem(storageKey) === "true") {
      setOpen(true, false);
    }
    buttons.forEach((button2) => {
      button2.addEventListener("click", () => {
        setOpen(group.getAttribute("data-open") !== "true", true);
      });
    });
  });
}
if (sidebar && button) {
  button.addEventListener("click", () => {
    const wasOpen = button.getAttribute("aria-pressed") === "true";
    sidebar.setAttribute("data-open", String(!wasOpen));
    button.setAttribute("aria-pressed", String(!wasOpen));
    sidebar.focus();
  });
  globalThis.addEventListener("keyup", (e) => {
    if (e.key === "Escape") {
      sidebar.setAttribute("data-open", "false");
      button.setAttribute("aria-pressed", "false");
    }
  });
}
var currentSidebarItem = sidebar.querySelector("a[data-active=true]") || sidebar.querySelector("[data-active=true]");
if (currentSidebarItem) {
  let currentElement = currentSidebarItem;
  let accordionContainer = null;
  let accordionToggle = null;
  while (currentElement && currentElement !== sidebar) {
    currentElement = currentElement.parentElement;
    if (currentElement && currentElement.tagName === "LI") {
      const toggleButton = currentElement.querySelector(
        ".sub-nav-toggle[data-accordion-toggle]"
      );
      if (toggleButton) {
        accordionContainer = currentElement;
        accordionToggle = toggleButton;
        break;
      }
    }
  }
  if (accordionContainer && accordionToggle) {
    const accordionId = accordionToggle.getAttribute("data-accordion-toggle");
    const allToggleButtons = document.querySelectorAll(
      ".sub-nav-toggle[data-accordion-toggle]"
    );
    allToggleButtons.forEach((otherToggleButton) => {
      const otherAccordionId = otherToggleButton.getAttribute(
        "data-accordion-toggle"
      );
      const otherParentLi = otherToggleButton.closest("li");
      if (otherToggleButton !== accordionToggle && otherParentLi) {
        otherParentLi.classList.remove("expanded");
        otherToggleButton.setAttribute("aria-expanded", "false");
        localStorage.setItem(`accordion-${otherAccordionId}`, "false");
      }
    });
    accordionContainer.classList.add("expanded");
    accordionToggle.setAttribute("aria-expanded", "true");
    localStorage.setItem(`accordion-${accordionId}`, "true");
  }
  setTimeout(() => {
    const aside = document.querySelector("aside");
    const nav = document.getElementById("nav");
    const sidebarElement = aside || nav;
    if (sidebarElement && sidebarElement.scrollTo) {
      try {
        const rect = currentSidebarItem.getBoundingClientRect();
        const sidebarRect = sidebarElement.getBoundingClientRect();
        const targetScrollTop = sidebarElement.scrollTop + rect.top - sidebarRect.top - sidebarRect.height / 2 + rect.height / 2;
        sidebarElement.scrollTo({
          top: Math.max(0, targetScrollTop),
          behavior: "smooth"
        });
      } catch (_e) {
      }
    }
  }, 300);
}
var desktopToc = document.querySelector("#toc");
if (desktopToc) {
  const tocItems = Array.from(document.querySelectorAll("#toc a"));
  const headings = Array.from(
    document.querySelectorAll(
      ".markdown-body :where(h1, h2, h3, h4, h5, h6)"
    )
  ).filter(
    (h) => h.id && document.querySelector(`#toc a[href="#${h.id}"]`)
  );
  if (headings.length > 0) {
    const updateActive = () => {
      const header = document.querySelector("header");
      const headerBottom = header ? header.getBoundingClientRect().bottom : 64;
      const line = headerBottom + (window.innerHeight - headerBottom) * 0.25;
      let current = headings[0];
      for (const h of headings) {
        if (h.getBoundingClientRect().top - line <= 0) {
          current = h;
        } else {
          break;
        }
      }
      const atBottom = window.innerHeight + Math.ceil(window.scrollY) >= document.documentElement.scrollHeight - 2;
      if (atBottom) {
        current = headings[headings.length - 1];
      }
      const activeHref = `#${current.id}`;
      tocItems.forEach((item) => {
        item.classList.toggle(
          "active",
          item.getAttribute("href") === activeHref
        );
      });
    };
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        updateActive();
        ticking = false;
      });
    };
    document.addEventListener("scroll", onScroll, { passive: true });
    globalThis.addEventListener("resize", onScroll, { passive: true });
    updateActive();
  }
}
