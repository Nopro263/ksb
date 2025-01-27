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
            <a href="#" id="logout">%logout%</a>
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