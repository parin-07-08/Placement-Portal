<template>
  <div class="container mt-4">
    <h3>Applicants for: {{ drive.title }}</h3>
    <div class="card border-dark"><div class="card-body">
      <div v-if="apps.length === 0" class="text-center text-muted mb-3">No applications received yet.</div>
      <div v-for="a in apps" :key="a.id" class="d-flex justify-content-between align-items-center border p-2 mb-2 rounded">
        <span>{{ a.student_name }} ({{ a.status }})</span>
        <button @click="$router.push(`/application/${a.id}`)" class="btn btn-outline-primary btn-sm">Review</button>
      </div>
      <button @click="$router.push('/company-dashboard')" class="btn btn-success font-weight-bold float-end mt-3">Back to Dashboard</button>
    </div></div>
  </div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      drive: {},
      apps: []
    };
  },

  mounted() {
    const driveId = Number(this.$route.params.id);

    api.request(`/drive/${driveId}`, "GET").then(drive => {
        if (drive) {
            this.drive = drive.data;
        }
    });

    api.request("/application", "GET").then(applications => {
        if (applications) {
            this.apps = applications.data.filter(a => a.drive_id === driveId);
        }
    });
}
};
</script>