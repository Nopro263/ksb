import Api from "./api.js";

const login = document.querySelector("#login-logout");
document.querySelector("#logout").addEventListener("click", (ev) => {
    Api.logout();
})

if(await Api.isLoggedIn()) {
    login.classList.add("loggedIn");
}