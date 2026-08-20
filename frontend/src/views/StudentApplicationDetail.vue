<template>
  <div class="container mt-4 d-flex justify-content-center"><div class="card border-dark p-4 w-100" style="max-width: 500px;">
    <h3 class="border-bottom pb-2 mb-3">Application Review</h3>

    <div class="mb-4">
      <p class="mb-1"><strong>Candidate:</strong> {{ application.student_name }}</p>
      <p class="mb-1"><strong>Education:</strong> {{ application.education }}</p>
      <p class="mb-1"><strong>Drive:</strong> {{ application.drive_title }}</p>
      <p><strong>Resume:</strong><a v-if="application.resume":href="application.resume" target="_blank" class="btn btn-primary btn-sm">View Resume</a><span v-else>No Resume Uploaded</span></p>
      <p class="mb-1"><strong>Current Status:</strong> {{ application.status }}</p>
    </div>

    <div class="mb-4">
      <label class="form-label font-weight-bold">Update Status:</label>
      <select v-model="status" class="form-select">
        <option value="Shortlist">Shortlist</option>
        <option value="Select">Select</option>
        <option value="Reject">Reject</option>
      </select>
    </div>

    <div class="d-flex justify-content-between border-top pt-3">
      <button @click="save" class="btn btn-success font-weight-bold btn-sm">Save</button>
      <button @click="$router.push('/company-dashboard')" class="btn btn-light border btn-sm">Back</button>
    </div>
  </div></div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      application: {},
      status: ""
    };
  },

  methods: {
    async save() {
      const res = await api.request(`/application/${this.$route.params.id}`, "PUT", {
        action: this.status
      });

      if (res) {
        alert("Application updated successfully.");
        this.$router.push("/company-dashboard");
      }
    }
  },

  async mounted() {
    const res = await api.request(`/application/${this.$route.params.id}`, "GET");

    if (res) {
      this.application = res.data;
      this.status = this.application.status;
    }
  }
};
</script>