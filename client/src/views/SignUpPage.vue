<template>
  <div>
    <h1>Sign Up</h1>
    <form @submit.prevent="signup">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="first_name" type="text" placeholder="First Name" required />
      <input v-model="last_name" type="text" placeholder="Last Name" required />
      <input v-model="phone_number" type="text" placeholder="Phone Number" />
      <input v-model="password" type="password" placeholder="Password" required />
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
          this.$router.push({ name: 'Login' });
        })
        .catch((error) => {
          this.errorMessage = error.response.data.error || 'An error occurred';
        });
    },
  },
};
</script>
