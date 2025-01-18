import Api from "./api.js";

await Api.checkLoggedIn();

const id = document.querySelector("#id");
const barcode = document.getElementById("barcode");
const creation_time = document.querySelector("#creation_time");
const sum = document.querySelector("#sum");
const msg = document.querySelector("#msg");


const invoice = await Api.create_invoice();
id.innerHTML = `Rechnung #${invoice.id}`;
creation_time.innerHTML = invoice.creation_time;

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    try {
        const article = await Api.sell_article(invoice.id, barcode.value);
        msg.innerHTML = "";
        if(article.has_already_been_sold) {
            msg.innerHTML = `Artikel #${article.id} '${article.name}' von #${article.list_id} bereits verkauft (${article.invoice_id})`;
            msg.classList.add("error");
        } else {
            msg.innerHTML = `Artikel #${article.id} '${article.name}' von #${article.list_id} verkauft`;
            msg.classList.remove("error");
            document.querySelector("tbody").innerHTML += `<tr><td>${article.name}</td><td>${article.size}</td><td>${article.price}€</td></tr>`;
            sum.innerHTML = parseInt(sum.innerHTML.substring(0, sum.innerHTML.length-1)) + article.price + "€"
        }

        barcode.focus();
    } catch({response, json}) {
        msg.innerHTML = "Error: " + json.detail;
        msg.classList.add("error");
    }
})