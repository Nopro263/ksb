import Api from './api.js'

await Api.checkLoggedIn();

const sellers = document.querySelector(".sellers > tbody");

const sell = await Api.get_users();

let i = 1;

sell.forEach(seller => {
    sellers.innerHTML += `<tr id="S${seller.id}" class="article"><td>${i++}</td><td>${seller.nickname}</td><td>${seller.first_name + " " + seller.last_name}</td><td>${seller.email}</td><td><a href="/seller?id=${seller.id}" class="success button">Ansehen</a></td></tr>`;
});