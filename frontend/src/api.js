const BASE_URL = "http://127.0.0.1:5000/api";

export const api = {
  async request(path, method = "GET", body = null) {
    const token = localStorage.getItem("token");

    const options = {
      method,
      headers: {
        "Content-Type": "application/json"
      }
    };

    if (token) {
      options.headers["Authentication-Token"] = token;
    }

    if (body && (method === "POST" || method === "PUT")) {
      options.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(BASE_URL + path, options);

      const data = response.status !== 204 ? await response.json() : {};

      if (!response.ok) {
        alert(data.message || "Request failed");
        return null;
      }

      return data;
    } catch (error) {
      console.error(error);
      alert("Unable to connect to the server.");
      return null;
    }
  }
};