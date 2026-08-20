<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-4">
      <h2>Welcome Admin</h2><button @click="logout" class="btn btn-sm btn-outline-dark">Logout</button>
      <input type="text" placeholder="Search..." v-model="query" class="form-control w-25" />
        <button class="btn btn-success me-2" @click="runTask">Run Daily Reminder</button>
        <input type="text" placeholder="Search..."v-model="query" class="form-control d-inline-block" style="width:200px;"/>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="card mb-4 border-dark"><div class="card-header bg-light font-weight-bold">Companies</div><div class="card-body">
          <div v-for="c in approvedCompanies.filter(x => x.name.toLowerCase().includes(query.toLowerCase()))" :key="c.id" class="d-flex justify-content-between align-items-center border p-2 mb-2 rounded">
            <span>{{ c.name }}</span><button @click="action('company', c.id, c.is_blacklisted ? 'unblacklist' : 'blacklist')" class="btn btn-danger btn-sm">{{ c.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}</button>
          </div>
        </div></div>

        <div class="card mb-4 border-dark"><div class="card-header bg-light font-weight-bold">Students</div><div class="card-body">
          <div v-for="s in students.filter(x => x.name.toLowerCase().includes(query.toLowerCase()))" :key="s.id" class="d-flex justify-content-between align-items-center border p-2 mb-2 rounded">
            <span>{{ s.name }}</span><button @click="action('student', s.id, s.is_blacklisted ? 'unblacklist' : 'blacklist')" class="btn btn-danger btn-sm">{{ s.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}</button>
          </div>
        </div></div>

        <div class="card border-dark"><div class="card-header bg-light font-weight-bold">Approvals</div><div class="card-body">
          <div v-for="c in pendingCompanies.filter(x => x.name.toLowerCase().includes(query.toLowerCase()))" :key="c.id" class="d-flex justify-content-between align-items-center border p-2 mb-2 rounded">
            <span>{{ c.name }}</span><div><button @click="action('company', c.id, 'approve')" class="btn btn-success btn-sm me-1">Approve</button><button @click="action('company', c.id, 'reject')" class="btn btn-secondary btn-sm">Reject</button></div>
          </div>
        </div></div>
      </div>

      <div class="col-md-6">
        <div class="card mb-4 border-dark"><div class="card-header bg-light font-weight-bold">Ongoing Drives</div>
          <table class="table table-bordered mb-0"><tbody>
            <tr v-for="d in drives" :key="d.id"><td>{{ d.title }}</td><td><button @click="$router.push(`/drive/${d.id}`)" class="btn btn-outline-primary btn-sm">Details</button></td></tr>
          </tbody></table>
        </div>

        <div class="card border-dark"><div class="card-header bg-light font-weight-bold">Student Applications</div>
          <table class="table table-bordered mb-0"><tbody>
            <tr v-for="a in applications" :key="a.id"><td>{{ a.student_name }}</td><td>{{ a.drive_title }}</td><td>{{ a.status }}</td></tr>
          </tbody></table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      query: "",
      approvedCompanies: [],
      pendingCompanies: [],
      students: [],
      drives: [],
      applications: []
    };
  },

  methods: {
    async load() {
      const companies = await api.request("/company", "GET");

      if (companies) {
        this.approvedCompanies = companies.data.filter(c => c.status === "Approved");
        this.pendingCompanies = companies.data.filter(c => c.status === "Pending");
      }


      const students = await api.request("/student", "GET");

      if (students) {
        this.students = students.data;
      }

      const drives = await api.request("/drive", "GET");

      if (drives) {
        this.drives = drives.data;
      }

      const applications = await api.request("/application", "GET");

      if (applications) {
        this.applications = applications.data;
      }
    },

    async action(type, id, action) {
      const res = await api.request(`/${type}/${id}`, "PUT", { action });

      if (res && res.status === "success") {
        this.load();
      }
    },
    async runTask() {
      const res = await api.request("/celery/demo", "POST");
      if(res){
        alert("Background task started.");
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