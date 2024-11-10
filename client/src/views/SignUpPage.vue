<!-- Prologue
Component Name: SignUpPage
Path: src/views/SignUpPage.vue

Description:
Provides a sign-up form for new users, allowing them to create an account with fields for email, name, phone number, and password.
-->

<template>
  <div>
    <h1>Sign Up</h1>
    <form @submit.prevent="signup">
      <input v-model="email" type="email" placeholder="Email" required/>
      <input v-model="first_name" type="text" placeholder="First Name" required/>
      <input v-model="last_name" type="text" placeholder="Last Name" required/>
      <input v-model="phone_number" type="text" placeholder="Phone Number"/>
      <input v-model="password" type="password" placeholder="Password" required/>
      <button type="submit">Sign Up</button>
    </form>
    <p>{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignUpPage',
  data() {
    return {
      email: '',
      first_name: '',
      last_name: '',
      phone_number: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    signup() {
      axios
          .post('/api/signup', {
            email: this.email,
            first_name: this.first_name,
            last_name: this.last_name,
            phone_number: this.phone_number,
            password: this.password,
          })
          .then(() => {
            // Optionally, log the user in automatically
            // Set authState.isAuthenticated = true if you log them in
            this.$router.push({name: 'Login'});
          })
          .catch((error) => {
            if (error.response && error.response.data && error.response.data.error) {
              this.errorMessage = error.response.data.error;
            } else if (error.message) {
              this.errorMessage = error.message;
            } else {
              this.errorMessage = 'An error occurred';
            }
          });
    },
  },
};
</script>
