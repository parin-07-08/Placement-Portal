import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/',
      name: 'index',
      component: () => import('../views/Index.vue')
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },

    {
      path: '/student/register',
      name: 'studentRegister',
      component: () => import('../views/StudentRegister.vue')
    },

    {
      path: '/company/register',
      name: 'companyRegister',
      component: () => import('../views/CompanyRegister.vue')
    },

    {
      path: '/admin-dashboard',
      name: 'adminDashboard',
      component: () => import('../views/AdminDashboard.vue')
    },

    {
      path: '/student-dashboard',
      name: 'studentDashboard',
      component: () => import('../views/StudentDashboard.vue')
    },

    {
      path: '/company-dashboard',
      name: 'companyDashboard',
      component: () => import('../views/CompanyDashboard.vue')
    },

    {
      path: '/company/:id',
      name: 'companyProfile',
      component: () => import('../views/CompanyProfileView.vue')
    },

    {
      path: '/drive/:id',
      name: 'driveDetails',
      component: () => import('../views/DriveDetails.vue')
    },

    {
      path: '/create-drive',
      name: 'createDrive',
      component: () => import('../views/CreateDrive.vue')
    },

    {
      path: '/history',
      name: 'studentHistory',
      component: () => import('../views/StudentHistory.vue')
    },

    {
      path: '/drive/:id/applications',
      name: 'reviewApplicants',
      component: () => import('../views/ReviewApplicants.vue')
    },

    {
      path: '/application/:id',
      name: 'applicationReview',
      component: () => import('../views/StudentApplicationDetail.vue')
    }

  ]
})

export default router