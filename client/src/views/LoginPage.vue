<!-- Prologue
Component Name: LoginPage
Path: src/views/LoginPage.vue

Description:
Provides a login form for users to authenticate, including fields for email and password, and displays error messages for failed login attempts.
-->

<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required/>
      <input v-model="password" type="password" placeholder="Password" required/>
      <button type="submit">Login</button>
    </form>
    <p>{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { authState } from '@/auth';

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    login() {
      axios
          .post('/api/login', {
            email: this.email,
            password: this.password,
          })
          .then((response) => {
            const token = response.data.access_token;
            localStorage.setItem('token', token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            authState.isAuthenticated = true; // Update the reactive state
            this.$router.push({name: 'Home'});
          })
          .catch((error) => {
            this.errorMessage = error.response.data.error || 'Invalid credentials';
          });
    },
  },
};
</script>

