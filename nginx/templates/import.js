import Api from "./api.js";


Api.checkLoggedIn();

const barcode = document.getElementById("barcode");

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    var response = await Api.import_article(barcode.value);
    console.log(response);
})