// document.addEventListener("DOMContentLoaded", function () {

//     const authLink = document.getElementById("auth-link");
//     const token = localStorage.getItem("access_token");

//     // data-login-url özelliğinden login URL'sini al
//     const loginLink = document.getElementById("login-link");
//     const loginUrl = loginLink ? loginLink.getAttribute("data-login-url") : null;
    
//     if (token) {
//         // Kullanıcı giriş yapmışsa Logout butonunu ekle
//         authLink.innerHTML = `<a href="javascript:void(0);" class="dropdown-item" id="logout-btn">Logout</a>`;

//         document.getElementById("logout-btn").addEventListener("click", function () {
//             localStorage.removeItem("access_token");  // Token'ı temizle
//             localStorage.removeItem("refresh_token");
//             window.location.href = loginUrl; // Login sayfasına yönlendir
//         });
//     } else {
//         // Kullanıcı giriş yapmamışsa Login butonunu ekle
//         authLink.innerHTML = `<a href="${loginUrl}" class="dropdown-item">Login</a>`; // Doğru login URL'i burada belirtiliyor
//     }
// });
