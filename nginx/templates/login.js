import Api from "./api.js";

Api.checkLoggedIn(true); // redirect if already logged in

const username = document.getElementById("username");
const password = document.getElementById("password");

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    await Api.login(username.value, password.value);
})