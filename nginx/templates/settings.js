import Api from "./api.js";

await Api.checkLoggedIn(); // redirect if already logged in

const username = document.getElementById("username");
const email = document.getElementById("email");
const first_name = document.getElementById("first_name");
const last_name = document.getElementById("last_name");
const phone = document.getElementById("phone");
const address = document.getElementById("address");
const password = document.getElementById("password");
const msg = document.getElementById("msg");

const user = await Api.get_self();

username.innerText = user.nickname;
email.value = user.email;
first_name.value = user.first_name;
last_name.value = user.last_name;
phone.value = user.phone_number;
address.value = user.address;

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    let content = "";
    let isValid = true;

    const c = (element, original, text) => {
        if(!element.value) {
            element.classList.add("invalid");
            isValid = false;
        } else {
            element.classList.remove("invalid");
        }
        if(element.value !== original) {
            if(content) {
                content += "<br/>"
            }
            content += `${text}: ${original ? original : "''"} → <b>${element.value ? element.value : "''"}</b>`
        }
    }
    
    c(email, user.email, "%email%");
    c(first_name, user.first_name, "%first-name%");
    c(last_name, user.last_name, "%last-name%");
    c(phone, user.phone_number, "%phone%");
    c(address, user.address, "%address%");

    if(!isValid) {
        return;
    }

    const data = (await Api.show_popup(
        "%save-changes%",
        content,
        [
            {
                type: "danger",
                text: "%discard-changes%",
                data: "no"
            },
            {
                type: "success",
                text: "%save-changes%",
                data: "yes"
            }
        ],
        undefined,
        "pass"
    )).data;


    if(data === "no") {
        history.back();
        return;
    } else if(data === "yes") {
        await Api.set_self(first_name.value, last_name.value, email.value, address.value, phone.value);
        window.location = "/";
    }
});