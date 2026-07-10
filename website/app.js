const searchInput = document.querySelector("#site-search");
const sections = [...document.querySelectorAll(".searchable-section")];
const navLinks = [...document.querySelectorAll(".nav-link")];
const emptyState = document.querySelector("#search-empty");
const searchStatus = document.querySelector(".search-status");
const menuButton = document.querySelector(".menu-button");
const sidebar = document.querySelector(".sidebar");

const normalize = (value) => value.toLocaleLowerCase("zh-Hant").trim();

function applySearch() {
  const query = normalize(searchInput.value);
  let matches = 0;

  sections.forEach((section) => {
    const haystack = normalize(`${section.dataset.search ?? ""} ${section.textContent}`);
    const visible = !query || haystack.includes(query);
    section.classList.toggle("is-filtered", !visible);
    if (visible) matches += 1;
  });

  emptyState.hidden = matches !== 0;
  searchStatus.textContent = query ? `找到 ${matches} 個相關章節` : "已清除搜尋";
  searchStatus.classList.add("visible");
  window.clearTimeout(applySearch.timeout);
  applySearch.timeout = window.setTimeout(() => searchStatus.classList.remove("visible"), 1600);
}

searchInput.addEventListener("input", applySearch);

document.addEventListener("keydown", (event) => {
  if (event.key === "/" && document.activeElement !== searchInput) {
    event.preventDefault();
    searchInput.focus();
  }
  if (event.key === "Escape" && document.activeElement === searchInput) {
    searchInput.value = "";
    applySearch();
    searchInput.blur();
  }
});

const sectionObserver = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((first, second) => second.intersectionRatio - first.intersectionRatio)[0];

    if (!visible) return;
    navLinks.forEach((link) => link.classList.toggle("active", link.hash === `#${visible.target.id}`));
  },
  { rootMargin: "-20% 0px -65% 0px", threshold: [0, 0.2, 0.5] },
);

sections.forEach((section) => sectionObserver.observe(section));

menuButton.addEventListener("click", () => {
  const open = sidebar.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(open));
});

navLinks.forEach((link) =>
  link.addEventListener("click", () => {
    sidebar.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
  }),
);

document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      const original = button.textContent;
      button.textContent = "已複製";
      window.setTimeout(() => (button.textContent = original), 1500);
    } catch {
      button.textContent = "複製失敗";
    }
  });
});
