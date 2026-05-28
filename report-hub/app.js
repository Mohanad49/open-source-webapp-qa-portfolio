const commands = {
  smoke: `python -m pytest -m smoke --browser chrome --headless \\\n  --html=reports/pytest-report.html --self-contained-html \\\n  --alluredir=reports/allure-results`,
  regression: `python -m pytest -m regression --browser chrome --headless \\\n  --html=reports/regression-report.html --self-contained-html \\\n  --alluredir=reports/allure-results`,
  allure: `allure generate reports/allure-results --clean -o reports/allure-report\nallure open reports/allure-report`,
};

const commandText = document.querySelector("#commandText");

document.querySelectorAll("[data-command]").forEach((button) => {
  button.addEventListener("click", () => {
    commandText.textContent = commands[button.dataset.command];
  });
});

const counters = document.querySelectorAll("[data-count]");
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const node = entry.target;
      const target = Number(node.dataset.count);
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 36));
      const timer = window.setInterval(() => {
        current += step;
        if (current >= target) {
          current = target;
          window.clearInterval(timer);
        }
        node.textContent = String(current);
      }, 24);
      observer.unobserve(node);
    });
  },
  { threshold: 0.6 }
);

counters.forEach((counter) => observer.observe(counter));
