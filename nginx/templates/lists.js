import Api from './api.js'

const listcontainer = document.querySelector(".listcontainer");
const create = document.querySelector("#create");

await Api.checkLoggedIn();

const main = async () => {
    const _lists = await Api.get_lists();
    listcontainer.innerHTML = "";

    for (let index = 0; index < _lists.length; index++) {
        const _list = _lists[index];
        const list = await Api.get_list(_list.id);
        const articleCount = list.articles.filter(a => !a.deleted).length;

        const div = document.createElement("a");
        div.classList.add("list");

        const id = document.createElement("p");
        id.classList.add("id");
        id.innerText = `#${index + 1}`;

        div.appendChild(id);

        const elementCount = document.createElement("p");
        elementCount.classList.add("elementCount");
        elementCount.innerText = `${articleCount}/${Api.getConfig().max_items_per_list}`;
        if(articleCount >= Api.getConfig().max_items_per_list) {
            div.classList.add("full");
        }

        if(articleCount < Api.getConfig().max_items_per_list && articleCount > Api.getConfig().max_items_per_list - 10) {
            div.classList.add("nearly-full");
        }

        div.appendChild(elementCount);

        div.href = `/list?id=${list.id}`;

        listcontainer.appendChild(div);
    }

    create.innerHTML = `Liste erstellen (${_lists.length}/${Api.getConfig().max_lists_per_user})`;

    if(_lists.length >= Api.getConfig().max_lists_per_user) {
        create.classList.add("full");
        create.disabled = true;
    }
}

create.addEventListener("click", async (ev) => {
    await Api.create_list();
    await main();
});

await main();