// ************************** Theme ******************************************

// document.addEventListener("DOMContentLoaded", function () {
//   const themeToggle = document.getElementById("theme-toggle");
//   const themeIcon = document.getElementById("theme-icon");
//   const body = document.body;

//   // Yaddaşdan mövcud temanı oxuyur
//   let currentTheme = localStorage.getItem("theme") || "light";
//   body.setAttribute("data-bs-theme", currentTheme);
//   updateIcon(currentTheme);

//   // Tema dəyişmə düyməsi
//   themeToggle.addEventListener("click", function () {
//     let newTheme =
//       body.getAttribute("data-bs-theme") === "light" ? "dark" : "light";
//     body.setAttribute("data-bs-theme", newTheme);
//     localStorage.setItem("theme", newTheme);
//     updateIcon(newTheme);
//   });

//   function updateIcon(theme) {
//     if (theme === "dark") {
//       themeIcon.classList.remove("bi-moon");
//       themeIcon.classList.add("bi-brightness-high");
//     } else {
//       themeIcon.classList.remove("bi-brightness-high");
//       themeIcon.classList.add("bi-moon");
//     }
//   }
// });

// ******************

document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");
  const body = document.body;

  // Yaddaşdan mövcud temanı oxuyur
  let currentTheme = localStorage.getItem("theme") || "light";
  body.setAttribute("data-bs-theme", currentTheme);
  updateTheme(currentTheme);

  // Tema dəyişmə düyməsi
  themeToggle.addEventListener("click", function () {
    let newTheme = body.getAttribute("data-bs-theme") === "light" ? "dark" : "light";
    body.setAttribute("data-bs-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateTheme(newTheme);
  });

  function updateTheme(theme) {
    if (theme === "dark") {
      themeIcon.classList.remove("bi-moon");
      themeIcon.classList.add("bi-brightness-high");

      // Bütün label-lərin rəngini ağ et
      document.querySelectorAll(".form-label").forEach(label => {
        label.style.color = "white";
      });

    } else {
      themeIcon.classList.remove("bi-brightness-high");
      themeIcon.classList.add("bi-moon");

      // Bütün label-lərin rəngini qara et
      document.querySelectorAll(".form-label").forEach(label => {
        label.style.color = "black";
      });
    }
  }
});


