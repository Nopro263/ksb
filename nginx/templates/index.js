import Api from "./api.js";

if(await Api.isLoggedIn()) {
    const config = await Api.getConfig();
    console.log(config)
    if(config.is_employee) {
        document.querySelector("main").innerHTML = `<form class="row"><input type="text" id="search" placeholder="%search%"/><input type=submit value="%start-search%" class="success"/></form>`;
        document.querySelector("form").addEventListener("submit", (ev) => {
            ev.preventDefault();
            ev.stopImmediatePropagation();
            window.location = "/search?q=" + encodeURIComponent(document.querySelector("#search").value);
        });

        document.querySelector("main").style["align-items"] = "center";
    }
}