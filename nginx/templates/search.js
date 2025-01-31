import Api from "./api.js";

await Api.checkLoggedIn();

const query = new URLSearchParams(window.location.search).get("q");

if(!query) {
    window.location = "/";
}

document.querySelector("#query").innerText = query;

const result = await Api.search_article(query);
const table = document.querySelector("tbody");
result.forEach(async (article) => {
    const list = await Api.get_list_bypass(article.list_id);
    const seller = await Api.get_user(list.owner_id);

    const c = (str) => {
        str = str + ""; // toString

        return str.replaceAll(query, `<b>${query}</b>`);
    }

    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${seller.nickname} ${c(list.id_in_user)}</td>
                <td>${article.id_in_list}</td>
                <td>${c(article.name)}</td>
                <td>${c(article.size)}</td>
                <td>${article.price}€</td>
                <td>${c(article.barcode)}</td>
                <td>${article.invoice_id ? c(article.invoice_id) : ""}</td>`;
    table.appendChild(tr);
});