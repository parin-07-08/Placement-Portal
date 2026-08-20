<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-4"><h2>Organization Dashboard</h2>
      <button @click="logout" class="btn btn-sm btn-outline-dark">Logout</button>
    </div>
    <div class="card mb-4 border-dark">
      <div class="card-header bg-light d-flex justify-content-between align-items-center font-weight-bold"><span>Upcoming Drives</span><button @click="$router.push('/create-drive')" class="btn btn-success btn-sm font-weight-bold">Create Drive</button></div>
      <table class="table table-bordered mb-0"><tbody>
        <tr v-for="d in upcoming" :key="d.id"><td>{{ d.title }}</td><td><button @click="$router.push(`/drive/${d.id}`)" class="btn btn-outline-secondary btn-sm me-1">Details</button><button @click="$router.push(`/drive/${d.id}/applications`)" class="btn btn-outline-primary btn-sm me-1">Applicants</button><button @click="complete(d.id)" class="btn btn-outline-success btn-sm">Mark Complete</button></td></tr>
      </tbody></table>
    </div>

    <div class="card border-dark">
      <div class="card-header bg-light font-weight-bold">Completed Drives</div>
      <table class="table table-bordered mb-0"><tbody>
        <tr v-for="d in closed" :key="d.id"><td>{{ d.title }}</td><td><button @click="$router.push(`/drive/${d.id}`)" class="btn btn-outline-secondary btn-sm me-2">Details</button><span class="badge bg-secondary">Completed</span></td></tr>
      </tbody></table>
    </div>
  </div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      upcoming: [],
      closed: []
    };
  },

  methods: {
    async load() {
      const res = await api.request("/drive", "GET");

      if (res) {
        this.upcoming = res.data.filter(d => d.status === "Active");
        this.closed = res.data.filter(d => d.status === "Completed");
      }
    },

    async complete(id) {
      const res = await api.request(`/drive/${id}`, "PUT", { action: "complete" });

      if (res) {
        this.load();
      }
    },

    async logout() {
      await api.request("/logout", "POST");
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  },

  mounted() {
    this.load();
  }
};
</script>