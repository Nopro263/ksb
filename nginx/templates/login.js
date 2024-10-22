import Api from "./api.js";

const username = document.getElementById("username");
const password = document.getElementById("password");

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    await Api.login(username.value, password.value);
})