<template>
  <div class="container d-flex flex-column justify-content-center align-items-center vh-100">
    <h1 class="mb-5">Placement Portal</h1>

    <div class="d-grid gap-3 col-4">
      <button @click="$router.push('/login')" class="btn btn-primary">Login</button>
      <button @click="$router.push('/student/register')" class="btn btn-outline-primary">Student Register</button>
      <button @click="$router.push('/company/register')" class="btn btn-outline-dark">Company Register</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Index"
};
</script>