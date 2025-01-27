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

lists.forEach(list => {
    main.innerHTML += `<div style="display: flex; flex-direction: column;"><h1>${user.nickname}${list.id}</h1><table class="articles" id="L${list.id}">
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
    
});