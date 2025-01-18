import Api from "./api.js";

Api.checkLoggedIn();

const barcode = document.getElementById("barcode");
const msg = document.getElementById("msg");

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    try {
        const article = await Api.import_article(barcode.value);
        msg.innerHTML = "";
        if(article.has_already_been_imported) {
            msg.innerHTML = `Artikel #${article.id} '${article.name}' von #${article.list_id} bereits importiert`;
            msg.classList.add("error");
        } else {
            msg.innerHTML = `Artikel #${article.id} '${article.name}' von #${article.list_id} importiert`;
            msg.classList.remove("error");
        }

        barcode.focus();
    } catch({response, json}) {
        msg.innerHTML = "Error: " + json.detail;
        msg.classList.add("error");
    }
})