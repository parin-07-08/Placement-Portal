<template>
  <div class="container mt-4 d-flex justify-content-center"><div class="card border-dark p-4 w-100" style="max-width: 500px;">
    <h3 class="text-center mb-4">Create a Drive</h3>
    <form @submit.prevent="submit">
      <div class="mb-3"><label class="form-label font-weight-bold">Title</label><input type="text" v-model="form.title" class="form-control" required /></div>
      <div class="mb-3"><label class="form-label font-weight-bold">Description</label><textarea v-model="form.description" class="form-control" rows="2" required></textarea></div>
      <div class="mb-3"><label class="form-label font-weight-bold">Salary (LPA)</label><input type="number" v-model="form.salary" class="form-control" required /></div>
      <div class="mb-3"><label class="form-label font-weight-bold">Location</label><input type="text" v-model="form.location" class="form-control" required /></div>
      <div class="mb-3"><label class="form-label font-weight-bold">Eligibility</label><input type="text" v-model="form.eligibility" class="form-control" required /></div>
      <div class="mb-3"><label class="form-label font-weight-bold">Deadline</label><input type="date" v-model="form.deadline" class="form-control" required /></div>
      <div class="d-flex justify-content-end">
        <button type="button" @click="$router.push('/company-dashboard')" class="btn btn-secondary me-2">Back</button>
        <button type="submit" class="btn btn-success font-weight-bold">Create Drive</button>
      </div>
    </form>
  </div></div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      form: {
        title: "",
        description: "",
        salary: "",
        location: "",
        eligibility: "",
        deadline: ""
      }
    };
  },

  methods: {
    async submit() {
      const res = await api.request("/drive", "POST", this.form);

      if (res) {
        alert("Drive created successfully.");
        this.$router.push("/company-dashboard");
      }
    }
  }
};
</script>