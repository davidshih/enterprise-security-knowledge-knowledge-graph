const searchInput = document.querySelector("#site-search");
const knowledgeCards = [...document.querySelectorAll(".knowledge-card")];
const emptyState = document.querySelector("#search-empty");
const searchStatus = document.querySelector(".search-status");
const menuButton = document.querySelector(".menu-button");
const menu = document.querySelector("#site-menu");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const normalize = (value) => value.toLocaleLowerCase("zh-Hant").trim();

function closeMenu() {
  menu.classList.remove("open");
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "開啟導覽選單");
}

function applySearch() {
  const query = normalize(searchInput.value);
  let matches = 0;

  knowledgeCards.forEach((card) => {
    const haystack = normalize(`${card.dataset.search ?? ""} ${card.textContent}`);
    const visible = !query || haystack.includes(query);
    card.hidden = !visible;
    if (visible) matches += 1;
  });

  emptyState.hidden = matches !== 0;
  searchStatus.textContent = query ? `找到 ${matches} 份文件` : "已清除搜尋";
  searchStatus.classList.add("visible");
  window.clearTimeout(applySearch.timeout);
  applySearch.timeout = window.setTimeout(() => searchStatus.classList.remove("visible"), 1600);
}

menuButton.addEventListener("click", () => {
  const open = menu.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute("aria-label", open ? "關閉導覽選單" : "開啟導覽選單");
});

menu.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
searchInput.addEventListener("input", applySearch);

document.addEventListener("keydown", (event) => {
  const typing = ["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName);

  if (event.key === "/" && !typing) {
    event.preventDefault();
    searchInput.focus();
    searchInput.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
  }

  if (event.key === "Escape") {
    closeMenu();
    if (document.activeElement === searchInput || searchInput.value) {
      searchInput.value = "";
      applySearch();
      searchInput.blur();
    }
  }
});

document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = "已複製";
    } catch {
      button.textContent = "複製失敗";
    }
    window.setTimeout(() => (button.textContent = original), 1500);
  });
});
