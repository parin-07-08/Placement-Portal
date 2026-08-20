<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-4"><h2>{{ company.name }}</h2><button @click="$router.back()" class="btn btn-sm btn-outline-dark">Back</button></div>

    <div class="card border-dark mb-4"><div class="card-header bg-light font-weight-bold">Overview</div><div class="card-body">
      <p><strong>Website:</strong> {{ company.website }}</p>
      <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>
      <p class="mb-0"><strong>Email:</strong> {{ company.email }}</p>
    </div></div>

    <div class="card border-dark"><div class="card-header bg-light font-weight-bold">Current Active Drives</div><div class="card-body">
      <p v-if="drives.length === 0" class="text-center text-muted mb-0">No active drives available.</p>
      <div v-for="d in drives" :key="d.id" class="d-flex justify-content-between align-items-center border p-2 mb-2 rounded">
        <span>{{ d.title }}</span><button @click="$router.push(`/drive/${d.id}`)" class="btn btn-outline-primary btn-sm">View Details</button>
      </div>
    </div></div>
  </div>
</template>

<script>
import { api } from '../api.js';

export default {
  props: ["company"],

  data() {
    return {
      drives: []
    };
  },

  methods: {
    async load() {
      const res = await api.request("/drive", "GET");

      if (res) {
        this.drives = res.data.filter(d => d.company_id === this.company.id && d.status === "Active");
      }
    }
  },

  mounted() {
    this.load();
  }
};
</script>