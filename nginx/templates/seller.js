import Api from "./api.js";

await Api.checkLoggedIn();

const search = new URLSearchParams(window.location.search);

if(search.get("id") === null) {
    window.location.pathname = "/sellers";
    throw new Error("");
    
}

const user = await Api.get_user(parseInt(search.get("id")));

const main = document.querySelector("main");

const lists = await Api.get_lists_of_user(user.id);

if(lists.length === 0) {
    main.innerHTML = `<h1 class="message">%no-items-found%</h1>`
}

lists.forEach(list => {
    main.innerHTML += `<div style="display: flex; flex-direction: column;"><div class="row"><h1>${user.nickname} ${list.id_in_user}</h1><button id="L${list.id}">%print%</button></div><table class="articles" id="L${list.id}">
    <thead class="thead">
        <tr>
            <td>#</td>
            <td>%name%</td>
            <td>%size%</td>
            <td>%price%</td>
        </tr>
    </thead>
    <tbody></tbody>
</table></div>`;
});

lists.forEach(async list => {
    const body = document.querySelector(`#L${list.id} > tbody`);
    const articles = (await Api.get_list_bypass(list.id)).articles;
    let i = 1;
    articles.forEach(article => {
        body.innerHTML += `<tr id="A${article.id}" class="article"><td>${i++}</td><td>${article.name}</td><td>${article.size}</td><td>${article.price}€</td></tr>`;
    });
    document.getElementById(`L${list.id}`).addEventListener("click", async (ev) => {
        const url = await Api.get_list_print_link_bypass(list.id);
        const w = window.open(url, 'print');
    });
});