<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 border-dark w-100" style="max-width: 450px;">
      <h2 class="text-center mb-4">Student Registration</h2>

      <form @submit.prevent="register">
        <div class="mb-3"><label class="form-label">Name</label><input type="text" v-model="form.name" class="form-control" required /></div>
        <div class="mb-3"><label class="form-label">Email</label><input type="email" v-model="form.email" class="form-control" required /></div>
        <div class="mb-3"><label class="form-label">Password</label><input type="password" v-model="form.password" class="form-control" required /></div>
        <div class="mb-3"><label class="form-label">Education</label><input type="text" v-model="form.education" class="form-control" required /></div>

        <div class="d-flex justify-content-between mt-4">
          <button type="button" @click="$router.push('/')" class="btn btn-outline-secondary">Back</button>
          <button type="submit" class="btn btn-success">Register</button>
        </div>

        <p class="text-center mt-3 mb-0">Already have an account? <a href="#" @click.prevent="$router.push('/login')">Login</a></p>
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
        password: "",
        name: "",
        education: ""
      }
    };
  },

  methods: {
    async register() {
      const res = await api.request("/student/register", "POST", this.form);

      if (res) {
        alert("Registration successful.");
        this.$router.push("/login");
      }
    }
  }
};
</script>