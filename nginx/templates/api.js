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
        if(response.ok) {
            resolve(json);
        } else {
            reject((response, json));
        }
    });
}

const sendAuthJSONCall = async (url, method, post_data, token) => {
    return sendApiCall(url, method, JSON.stringify(post_data), "application/json", {
        "Authorization": "Bearer " + token
    });
}

class Api {
    token = "";
    static async login(username, password) {
        let response = await sendApiCall("/token", "POST", new URLSearchParams({
            'username': username,
            'password': password,
            'grant_type': 'password'
        }), "application/x-www-form-urlencoded");

        Api.token = response.access_token;
        localStorage.setItem("token", Api.token);

        this.redirectToTarget();

        return response.access_token;
    }

    static async create_invoice() {
        return await sendAuthJSONCall("/invoice", "PUT", undefined, Api.token);
    }

    static async import_article(article_id) {
        return await sendAuthJSONCall("/import", "POST", {"articleId": article_id}, Api.token);
    }

    static async checkLoggedIn() {
        try {
            await sendAuthJSONCall("/token", "GET", undefined, Api.token);
        } catch (error) {
            var targetUrl = new URL(window.location);

            targetUrl.pathname = "login";

            var encoded = encodeURIComponent(window.location);
            targetUrl.searchParams.set("redirect", encoded);

            window.location = targetUrl;
        }
    }

    static redirectToTarget() {
        var url = new URL(window.location);
        var redirect = url.searchParams.get("redirect");

        var targetUrl = new URL(decodeURIComponent(redirect));

        if(targetUrl.host != window.location.host) {
            return;
        }

        window.location = targetUrl;
    }
}

Api.token = localStorage.getItem("token");

export default Api;