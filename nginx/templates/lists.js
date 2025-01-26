import Api from './api.js'

const listcontainer = document.querySelector("tbody");
const create = document.querySelector("#create");

await Api.checkLoggedIn();
if(!Api.getConfig()) {
    throw new Error("???");
    
}
if(Api.getConfig().is_employee) {
    window.location.pathname = "/";
    throw new Error("");
}

const main = async () => {
    const _lists = await Api.get_lists();
    const self = await Api.get_self();

    listcontainer.innerHTML = "";

    for (let index = 0; index < _lists.length; index++) {
        const _list = _lists[index];
        const list = await Api.get_list(_list.id);
        const articleCount = list.articles.filter(a => !a.deleted).length;

        const tr = document.createElement("tr");

        const id = document.createElement("td");
        id.innerText = `${_list.id_in_user}`;

        tr.appendChild(id);

        const name = document.createElement("td");
        name.innerText = `${self.nickname}${_list.id_in_user}`;
        tr.appendChild(name);

        const elementCount = document.createElement("td");
        elementCount.innerText = `${articleCount}/${Api.getConfig().max_items_per_list}`;

        if(articleCount >= Api.getConfig().max_items_per_list) {
            tr.classList.add("full");
        }

        if(articleCount < Api.getConfig().max_items_per_list && articleCount > Api.getConfig().max_items_per_list - 10) {
            tr.classList.add("nearly-full");
        }

        tr.appendChild(elementCount);

        const openTd = document.createElement("td");
        const btn = document.createElement("button");
        btn.classList.add("success");
        btn.innerText = `%open%`;

        btn.addEventListener("click", (ev) => {
            window.location = `/list?id=${_list.id}`;
        });

        openTd.appendChild(btn);

        tr.appendChild(openTd);

        listcontainer.appendChild(tr);
    }

    create.innerHTML = `%create-list% (${_lists.length}/${Api.getConfig().max_lists})`;

    if(_lists.length >= Api.getConfig().max_lists) {
        create.classList.add("full");
        create.disabled = true;
    }
}

create.addEventListener("click", async (ev) => {
    const answer = await Api.show_popup(
        "%are-you-sure%",
        "%information-list-price%",
        [
            {
                type: "information",
                text: "%create-it%",
                data: "yes"
            },
            {
                type: "danger",
                text: "%dont-do-it%",
                data: "no"
            },
            {
                type: "",
                text: "%more-information%",
                data: "more"
            }
        ],
        undefined,
        "no"
    );

    if(answer.data == "more") {
        window.open("https://www.kindersachenboer.se/ablauf", "_blank");
    }

    if(answer.data != "yes") {
        return;
    }

    await Api.create_list();
    await main();
});

await main();