// document.addEventListener("DOMContentLoaded", function () {
//   const form = document.querySelector("form");
//   const errorMessage = document.getElementById("error-message"); // Hata mesajı div'ini al

//   form.addEventListener("submit", async function (event) {
//     event.preventDefault(); // Sayfanın yenilenmesini engelle

//     const formData = new FormData(form);
//     const response = await fetch(
//       "http://127.0.0.1:8000/api/v1/account/login/",
//       {
//         method: "POST",
//         body: formData,
//         headers: {
//           "X-CSRFToken": getCookie("csrftoken"), // CSRF güvenliği için
//         },
//       }
//     );

//     if (response.ok) {
//       const data = await response.json();
//       localStorage.setItem("access_token", data.access); // JWT token'ı kaydet
//       localStorage.setItem("refresh_token", data.refresh);
//       window.location.href = data.redirect; // Home sayfasına yönlendir
//     } else {
//         errorMessage.textContent = "İstifadəçi adı və ya şifrə yalnışdır.";
//         errorMessage.style.visibility = "visible";  // Görünür yap
//         errorMessage.style.opacity = "1";
//     }
//   });

//   // CSRF Token al
//   function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== "") {
//       const cookies = document.cookie.split(";");
//       for (let i = 0; i < cookies.length; i++) {
//         const cookie = cookies[i].trim();
//         if (cookie.startsWith(name + "=")) {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//         }
//       }
//     }
//     return cookieValue;
//   }
// });
