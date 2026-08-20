<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 border-dark w-100" style="max-width: 400px;">
      <h2 class="text-center mb-4">Login</h2>

      <form @submit.prevent="login">
        <div class="mb-3"><label class="form-label">Email</label><input type="email" v-model="form.email" class="form-control" required /></div>
        <div class="mb-3"><label class="form-label">Password</label><input type="password" v-model="form.password" class="form-control" required /></div>

        <button type="submit" class="btn btn-primary w-100">Login</button>

        <div class="text-center mt-3">
          <button type="button" @click="$router.push('/')" class="btn btn-link">Back</button>
        </div>

        <p class="text-center mt-2 mb-0">Don't have an account? <a href="#" @click.prevent="$router.push('/student/register')">Register</a></p>
      </form>
    </div>
  </div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      form: {
        email: "",
        password: ""
      }
    };
  },

  methods: {
    async login() {
      const res = await api.request("/login", "POST", this.form);

      if (res) {
        const user = res.user_details;

        localStorage.setItem("token", user.auth_token);
        localStorage.setItem("user_type", user.user_type);
        localStorage.setItem("user_id", user.id);

        if (user.user_type === "admin") {
          this.$router.push("/admin-dashboard");
        }
        else if (user.user_type === "company") {
          this.$router.push("/company-dashboard");
        }
        else {
          this.$router.push("/student-dashboard");
        }
      }
    }
  }
};
</script>