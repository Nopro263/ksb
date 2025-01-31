const sendApiCall = async (url, method, post_data, content_type, headers) => {
    if(!headers) {
        headers = {}
    }
    headers["Content-Type"] = content_type
    let response = await fetch("/api" + url, {
        method: method,
        cache: "no-store",
        headers: headers,

        body: post_data
    });

    let json = await response.json();

    return new Promise((resolve, reject) => {
        if(response.ok && response.status >= 200 && response.status < 300) {
            resolve(json);
        } else {
            reject({response, json});
        }
    });
}

const sendAuthJSONCall = async (url, method, post_data, token) => {
    return sendApiCall(url, method, post_data ? JSON.stringify(post_data) : post_data, post_data ? "application/json" : undefined, {
        "Authorization": "Bearer " + token
    });
}

class Api {
    token = "";
    _popup_reject = null;
    static async login(username, password) {
        let response = await sendApiCall("/user/login", "POST", new URLSearchParams({
            'username': username,
            'password': password,
            'grant_type': 'password'
        }), "application/x-www-form-urlencoded");

        Api.token = response.access_token;
        localStorage.setItem("token", Api.token);

        this.redirectToTarget("/");

        return response.access_token;
    }

    static getConfig() {
        return this.config;
    }

    static async get_available_usernames() {
        return await sendApiCall("/user/usernames", "GET");
    }

    static async register(first_name, last_name, email, nickname, password, address, phone) {
        let data = {first_name, last_name, email, nickname, password, address, phone_number: phone};
        return await sendApiCall("/user/register", "PUT", JSON.stringify(data), "application/json");
    }

    static async get_self() {
        return await sendAuthJSONCall("/user/me", "GET", undefined, Api.token);
    }

    static async set_self(first_name, last_name, email, address, phone) {
        let data = {first_name, last_name, email, address, phone_number: phone};
        return await sendAuthJSONCall("/user/me", "POST", data, Api.token);
    }

    static async get_users() {
        return await sendAuthJSONCall("/user/users", "GET", undefined, Api.token);
    }

    static async get_articles(userId) {
        return await sendAuthJSONCall("/user/" + userId + "/articles", "GET", undefined, Api.token);
    }

    static async create_list() {
        return await sendAuthJSONCall("/list", "PUT", undefined, Api.token);
    }

    static async create_article(list, name, size, price) {
        let data = {name, size, price};
        return await sendAuthJSONCall("/list/" + list, "POST", data, Api.token);
    }

    static async get_list(list) {
        return await sendAuthJSONCall("/list/" + list, "GET", undefined, Api.token);
    }

    static async get_list_print_link(id) {
        return await sendAuthJSONCall("/list/" + id + "/print", "GET", undefined, Api.token);
    }

    static async get_lists() {
        return await sendAuthJSONCall("/list", "GET", undefined, Api.token);
    }

    static async delete_article(list, article) {
        return await sendAuthJSONCall("/list/" + list + "/" + article, "DELETE", undefined, Api.token);
    }

    static async import_article(barcode) {
        return await sendAuthJSONCall("/article/" + barcode + "/import", "POST", undefined, Api.token);
    }

    static async search_article(query) {
        return await sendAuthJSONCall("/article/search", "POST", {query}, Api.token);
    }

    static async create_invoice() {
        return await sendAuthJSONCall("/invoice/new", "POST", undefined, Api.token);
    }

    static async sell_article(invoice, barcode) {
        return await sendAuthJSONCall("/invoice/" + invoice + "/sell/" + barcode, "POST", undefined, Api.token);
    }

    static async get_invoice(id) {
        return await sendAuthJSONCall("/invoice/" + id, "GET", undefined, Api.token);
    }

    static async get_invoice_details(id) {
        return await sendAuthJSONCall("/invoice/" + id + "/meta", "GET", undefined, Api.token);
    }

    static async get_invoice_print_link(id) {
        return await sendAuthJSONCall("/invoice/" + id + "/print", "GET", undefined, Api.token);
    }

    static async get_user(id) {
        return await sendAuthJSONCall("/user/" + id, "GET", undefined, Api.token);
    }

    static async get_lists_of_user(id) {
        return await sendAuthJSONCall("/list/of/" + id, "GET", undefined, Api.token);
    }

    static async get_list_bypass(id) {
        return await sendAuthJSONCall("/list/" + id + "/bypass", "GET", undefined, Api.token);
    }

    static async isLoggedIn() {
        try {
            await sendAuthJSONCall("/user/me", "GET", undefined, Api.token);
            let d = await sendAuthJSONCall("/user/config", "GET", undefined, Api.token);
            this.config = d;
            return true;
        } catch (error) {
            return false;
        }
    }

    static async checkLoggedIn(r=false) {
        if(await this.isLoggedIn()) {
            if(r) {
                this.redirectToTarget("/");
            }
        } else if(!r) {
            var targetUrl = new URL(window.location);

            targetUrl.pathname = "login";

            var encoded = encodeURIComponent(window.location);
            targetUrl.searchParams.set("redirect", encoded);

            window.location = targetUrl;
        }
    }

    static redirectToTarget(d=undefined) {
        var url = new URL(window.location);
        var redirect = url.searchParams.get("redirect");
        if(redirect == null) {
            if(d !== undefined) {
                window.location.pathname = d;
                //window.location.search = "";
                throw new Error("");
            }
            return;
        }

        var targetUrl = new URL(decodeURIComponent(redirect));

        if(targetUrl.host != window.location.host) {
            return;
        }

        window.location = targetUrl;
    }

    static logout() {
        Api.token = undefined;
        localStorage.removeItem("token");
        window.location.pathname = "/";
        window.location.reload();
    }

    static async show_popup(title, content, options=[], image=undefined, default_data=undefined) {
        Api.close_popup();

        const popup = document.querySelector(".popup");
        const c = popup.querySelector(".content");
        const h1  = popup.querySelector("h1");
        const img = popup.querySelector("img");
        const answers = popup.querySelector(".answers");
        answers.innerHTML = "";

        h1.innerText = title;
        c.innerHTML = content;
        img.src = image ? image : "https://cdn-icons-png.flaticon.com/512/4201/4201973.png";

        popup.style.display = "flex";

        return new Promise((resolve, reject) => {
            Api._popup_reject = reject;
            for (const option of options) {
                const element = document.createElement("button");
                if(option.type) {
                    element.classList.add(option.type);
                }
                element.innerText = option.text;
                element.addEventListener("click", (ev) => {
                    Api._popup_reject = null;
                    this.close_popup();
                    resolve({
                        "event": ev,
                        "data": option.data
                    });
                });
    
                answers.appendChild(element);
            }

            popup.addEventListener("click", (ev) => {
                Api._popup_reject = null;
                    this.close_popup();
                    resolve({
                        "event": ev,
                        "data": default_data
                    });
            })
        });
    }

    static close_popup() {
        const popup = document.querySelector(".popup");
        popup.style.display = "none";
        if(Api._popup_reject) {
            Api._popup_reject("closed");
            Api._popup_reject = null;
        }
    }
}

Api.token = localStorage.getItem("token");

export default Api;