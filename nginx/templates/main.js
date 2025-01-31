import Api from "./api.js";

if(await Api.isLoggedIn()) {
    const config = Api.getConfig();
    if(config.is_employee) {
        document.querySelector("nav").innerHTML = `<a class="nav-component right" href="/">%home%</a>
        <a class="nav-component" href="/sellers">%sellers%</a>
        <a class="nav-component" href="/sell">%sell%</a>
        <a class="nav-component left" href="/import">%import%</a>

        <div class="nav-component" id="login-logout">
            <a href="/login" id="login">%login%</a>
            <div class="nav-dropdown">
                <div class="nav-item nav-name">%account%</div>
                <div class="nav-items">
                    <a class="nav-item" id="settings" href="/settings">%settings%</a>
                    <div class="nav-item" id="logout">%logout%</div>
                    <div class="nav-item row">
                        <button id="lang-de">DE</button>
                        <button id="lang-en">EN</button>
                    </div>
                </div>
            </div>
        </div>`
    }

    const login = document.querySelector("#login-logout");
    login.classList.add("loggedIn");
}

document.querySelector("#logout").addEventListener("click", (ev) => {
    Api.logout();
})

const nav_component = document.querySelector(`a.nav-component[href="${window.location.pathname}"]`) || (window.location.pathname === "/list" ? document.querySelector(`a.nav-component[href="/lists"]`) : undefined);

if(nav_component) {
    nav_component.classList.add("active");
}

const lang = {}

lang["de"] = document.querySelector("#lang-de");
lang["en"] = document.querySelector("#lang-en");

const setLang = (lang) => {
    document.cookie = "language=" + lang;

    window.location.reload();
}

const getCookieValue = (name) => { // https://stackoverflow.com/a/25490531
    return document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || '';
}

const getLang = () => {
    const value = getCookieValue("language");
    const lang = navigator.language || navigator.userLanguage;
    return value || lang;
}

lang["de"].addEventListener("click", () => {
    setLang("de");
});

lang["en"].addEventListener("click", () => {
    setLang("en");
});

const l = getLang();
console.log(lang[l]);
if(lang[l]) {
    lang[l].classList.add("active");
}