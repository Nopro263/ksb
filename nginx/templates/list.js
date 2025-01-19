import Api from './api.js'

await Api.checkLoggedIn();

const articles = document.querySelector(".articles > tbody");
const name = document.getElementById("name");
const size = document.getElementById("size");
const price = document.getElementById("price");

const next_num = document.querySelector("#next-num");

const args = new URLSearchParams(window.location.search);
const id = args.get("id");

const main = async () => {
    let list;
    try {
        list = await Api.get_list(id);
    } catch({response, json}) {
        alert(json.detail);
        window.location.pathname = "/";
        window.location.search = "";
        return;
    }

    articles.innerHTML = "";

    let i = 1;

    let c = 0;

    for (const article of list.articles) {
        articles.innerHTML += `<tr id="A${article.id}" class="article"><td>${i}</td><td>${article.name}</td><td>${article.size}</td><td>${article.price}€</td><td>${article.deleted ? "" : "<button>X</button>"}</td></tr>`;
        
        if(article.deleted) {
            articles.querySelector(`#A${article.id}`).classList.add("deleted");
        } else {
            c++;
        }
        
        i++;
    };

    next_num.innerHTML = i;


    for (const article of list.articles) {
        const b = document.querySelector(`.articles > tbody > #A${article.id} > td > button`);
        if(!b) {
            continue;
        }
        b.addEventListener("click", async (ev) => {
            await Api.delete_article(id, article.id);
            main();
        });
    }

    if(c+1 > Api.getConfig().max_items_per_list) {
        document.querySelector("input[type=submit]").disabled = true;
    } else {
        document.querySelector("input[type=submit]").disabled = false;
    }
}

main();


document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    await Api.create_article(id, name.value, size.value, price.value);
    main();
});