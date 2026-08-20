<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-4">
      <h2>Student Dashboard</h2>
      <div><a href="#" @click.prevent="$router.push('/history')" class="me-3">History</a><input type="file" ref="resume"/><button class="btn btn-success" @click="uploadResume">Upload Resume</button><button @click="logout" class="btn btn-sm btn-outline-dark">Logout</button></div>
    </div>
    <div class="card mb-4 border-dark"><div class="card-header bg-light font-weight-bold">Drives Available</div><div class="card-body">
      <div v-if="drives.length === 0" class="text-center text-muted">No active Drives.</div>
      <div v-for="d in drives" :key="d.id" class="d-flex justify-content-between align-items-center border p-2 mb-2 rounded">
        <span>{{ d.title }}</span><button @click="$router.push(`/drive/${d.id}`)" class="btn btn-outline-primary btn-sm">View Details</button>
      </div>
    </div></div>

    <div class="card border-dark"><div class="card-header bg-light font-weight-bold">My Applications</div>
      <table class="table table-bordered mb-0"><tbody>
        <tr v-if="apps.length === 0"><td colspan="2" class="text-center text-muted">No applications yet.</td></tr>
        <tr v-for="a in apps" :key="a.id">
          <td>{{ a.drive_title }} ({{ a.company_name }})</td>
          <td>
            <span :class="{
              'badge bg-secondary': a.status === 'Applied',
              'badge bg-warning text-dark': a.status === 'Shortlist',
              'badge bg-success': a.status === 'Select',
              'badge bg-danger': a.status === 'Reject'
            }">{{ a.status }}</span>
          </td>
        </tr>
      </tbody></table>
    </div>
  </div>
</template>

<script>
import { api } from '../api.js';

export default {
  data() {
    return {
      drives: [],
      apps: []
    };
  },

  methods: {
    async load() {
      const drives = await api.request("/drive", "GET");

      if (drives) {
        this.drives = drives.data;
      }

      const applications = await api.request('/application', 'GET');

      if (applications) {
        this.apps = applications.data;
      }
    },
    async uploadResume(){

      const file=this.$refs.resume.files[0];

      if(!file){
        alert("Choose a file");
        return;
      }

      const formData=new FormData();

      formData.append("resume",file);

      const token=localStorage.getItem("token");

      const response=await fetch(
        "http://127.0.0.1:5000/api/student/upload_resume",
        {
            method:"POST",

            headers:{
                "Authentication-Token":token
            },

            body:formData
        }
      );

    const data=await response.json();

    alert(data.message);

},
    async logout() {
      await api.request("/logout", "POST");
      localStorage.removeItem("token");
      localStorage.removeItem("user_type");
      localStorage.removeItem("user_id");
      this.$router.push("/login");
    }
  },

  mounted() {
    this.load();
  }
};
</script>