import Api from "./api.js";

if(await Api.isLoggedIn()) {
    const config = await Api.getConfig();
    console.log(config)
    if(config.is_employee) {
        const stats = await Api.get_stats();

        document.querySelector("main").innerHTML = `<div class="stats col"><div class="row">%imported%: ${stats.imported}/${stats.amount_articles} (${Math.floor(stats.imported / stats.amount_articles * 10000) / 100}%) %articles%</div><div class="row">%sold%: ${stats.sold}/${stats.amount_articles} (${Math.floor(stats.sold / stats.amount_articles * 10000) / 100}%) %articles%</div><div class="row">%sales%: ${stats.sold_value}€/${stats.total_value}€ (${Math.floor(stats.sold_value / stats.total_value * 10000) / 100}%)</div></div><form class="row"><input type="text" id="search" placeholder="%search%"/><input type=submit value="%start-search%" class="success"/></form>`;
        document.querySelector("form").addEventListener("submit", (ev) => {
            ev.preventDefault();
            ev.stopImmediatePropagation();
            window.location = "/search?q=" + encodeURIComponent(document.querySelector("#search").value);
        });

        document.querySelector("main").style["align-items"] = "center";
        document.querySelector("main").classList.add("col")
    }
}