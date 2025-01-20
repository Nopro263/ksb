import Api from "./api.js";

if(await Api.isLoggedIn()) {
    const config = Api.getConfig();
    if(config.is_employee) {
        document.querySelector("nav").innerHTML = `<a class="nav-component right" href="/">Home</a>
        <a class="nav-component" href="/sellers">Verkäufer</a>
        <a class="nav-component" href="/sell">Verkaufen</a>
        <a class="nav-component left" href="/import">Importieren</a>

        <div class="nav-component" id="login-logout">
            <a href="/login" id="login">Login</a>
            <a href="#" id="logout">Logout</a>
        </div>`
    }

    const login = document.querySelector("#login-logout");
    login.classList.add("loggedIn");
}

document.querySelector("#logout").addEventListener("click", (ev) => {
    Api.logout();
})

const nav_component = document.querySelector(`a.nav-component[href="${window.location.pathname}"]`);

if(nav_component) {
    nav_component.classList.add("active");
}