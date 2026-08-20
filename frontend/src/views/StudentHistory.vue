<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3"><h3>Application History</h3><button @click="$router.push('/student-dashboard')" class="btn btn-outline-primary btn-sm">Back</button></div>
    <button class="btn btn-success"@click="exportCSV">Download CSV</button>
  </div>
  <div>
    <table class="table table-bordered bg-white">
      <thead class="table-light"><tr><th>Drive Name</th><th>Status</th></tr></thead>
      <tbody>
        <tr v-if="history.length === 0"><td colspan="2" class="text-center">No applications found.</td></tr>
        <tr v-for="h in history" :key="h.id">
          <td>{{ h.drive_title }}</td>
          <td :class="{
            'font-weight-bold text-secondary': h.status === 'Applied',
            'font-weight-bold text-warning': h.status === 'Shortlist',
            'font-weight-bold text-success': h.status === 'Select',
            'font-weight-bold text-danger': h.status === 'Reject'
          }">{{ h.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      history: []
    };
  },

  methods: {

    async load() {

        const res = await api.request("/application", "GET");

        if(res){
            this.history = res.data;
        }

    },

    exportCSV() {

    let csv = "Drive,Company,Status,Applied On\n";

    this.history.forEach(h => {

        csv += `"${h.drive_title}","${h.company_name}","${h.status}","${h.date}"\n`;

    });

    const blob = new Blob([csv], {
        type: "text/csv"
    });

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = "ApplicationHistory.csv";

    a.click();

    window.URL.revokeObjectURL(url);

}

}
};
</script>