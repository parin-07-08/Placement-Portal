<template>
  <div class="container mt-4 d-flex justify-content-center"><div class="card border-dark p-4 w-100" style="max-width: 500px;">
    <div class="border-bottom pb-2 mb-3">
      <h3>{{ drive.title }}</h3>
      <small class="text-muted">Job Opportunity</small>
    </div>

    <div class="mb-4">
      <p class="p-2 border rounded bg-light">{{ drive.description }}</p>
      <p><strong>Package:</strong> ₹ {{ drive.salary }} LPA</p>
      <p><strong>Location:</strong> {{ drive.location }}</p>
      <p><strong>Eligibility:</strong> {{ drive.eligibility }}</p>
      <p><strong>Deadline:</strong> {{ drive.deadline }}</p>
    </div>

    <div class="d-flex justify-content-between">
      <button v-if="userRole === 'student' && drive.status === 'Active'"@click="apply"class="btn btn-outline-primary px-4">Apply</button>
      <button @click="$router.back()" class="btn btn-light border px-4">Go Back</button>
    </div>
  </div></div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      drive: {},
      userRole: localStorage.getItem("user_type")
    };
  },

  methods: {
    async apply() {
      const res = await api.request("/application", "POST", {
        drive_id: this.$route.params.id
      });

      if (res) {
        alert("Application submitted successfully.");
        this.$router.back();
      }
    }
  },

  async mounted() {
    const res = await api.request(`/drive/${this.$route.params.id}`, "GET");

    if (res) {
      this.drive = res.data;
    }
  }
};
</script>