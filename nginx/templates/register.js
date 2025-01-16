import Api from "./api.js";

await Api.checkLoggedIn(true); // redirect if already logged in

const username = document.getElementById("username");
const email = document.getElementById("email");
const first_name = document.getElementById("first_name");
const last_name = document.getElementById("last_name");
const password = document.getElementById("password");
const password2 = document.getElementById("password2");
const msg = document.getElementById("msg");

const usernames = await Api.get_available_usernames();
usernames.forEach(element => {
    username.innerHTML += `<option value="${element}">${element}</option>`;
});

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    if(password.value !== password2.value) {
        return;
    }
    try {
        document.querySelector("form").classList.remove("wrong");
        await Api.register(first_name.value, last_name.value, email.value, username.value, password.value);
        await Api.login(username.value, password.value);
    } catch({response, json}) {
        document.querySelector("form").classList.add("wrong");
        msg.innerText = json.detail;
    }
});