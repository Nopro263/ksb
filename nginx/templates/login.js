import Api from "./api.js";

Api.checkLoggedIn(true); // redirect if already logged in

const username = document.getElementById("username");
const password = document.getElementById("password");
const msg = document.getElementById("msg");

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    try {
        document.querySelector("form").classList.remove("wrong");
        await Api.login(username.value, password.value);
    } catch({response, json}) {
        if(response.status == 403) {
            document.querySelector("form").classList.add("wrong");
            msg.innerText = json.detail;
            return;
        }
    }
})