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

    static async register(first_name, last_name, email, nickname, password) {
        let data = {first_name, last_name, email, nickname, password};
        return await sendApiCall("/user/register", "PUT", JSON.stringify(data), "application/json");
    }

    static async get_self() {
        return await sendAuthJSONCall("/user/me", "GET", undefined, Api.token);
    }

    static async set_self(first_name, last_name, email) {
        let data = {first_name, last_name, email};
        return await sendAuthJSONCall("/user/me", "POST", data, Api.token);
    }

    // /user/users
    // /user/{id}/articles

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

    static async get_lists() {
        return await sendAuthJSONCall("/list", "GET", undefined, Api.token);
    }

    static async delete_article(list, article) {
        return await sendAuthJSONCall("/list/" + list + "/" + article, "DELETE", undefined, Api.token);
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
        if(!redirect) {
            if(d) {
                window.location.pathname = d;
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
}

Api.token = localStorage.getItem("token");

export default Api;