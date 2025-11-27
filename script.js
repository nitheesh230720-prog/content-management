function showPage(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(pageId).classList.add('active');
}

document.addEventListener("DOMContentLoaded", function () {
  const page = document.body.getAttribute("data-page");

  if (page === "register") {
    showPage("registerPage");
  } else if (page === "home") {
    showPage("homePage");
  } else {
    showPage("loginPage");
  }
});