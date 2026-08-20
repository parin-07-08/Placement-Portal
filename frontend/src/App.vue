<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4 fixed-bottom">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/">Placement Portal</RouterLink>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/">Home</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/register">Student Register</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/company/register">Company Register</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <RouterView />
  </div>
</template>

<style>
body{
    background-color:#f8f9fa;
}
</style>