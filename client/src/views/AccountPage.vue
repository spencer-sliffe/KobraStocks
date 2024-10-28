<template>
  <div>
    <h1>Account Details</h1>
    <div v-if="user">
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>First Name:</strong> {{ user.first_name }}</p>
      <p><strong>Last Name:</strong> {{ user.last_name }}</p>
      <p><strong>Phone Number:</strong> {{ user.phone_number }}</p>
      <p><strong>Budget:</strong> {{ user.budget }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AccountPage',
  data() {
    return {
      user: null,
    };
  },
  created() {
    this.fetchUserDetails();
  },
  methods: {
    fetchUserDetails() {
      axios
        .get('/api/user')
        .then((response) => {
          this.user = response.data;
        })
        .catch((error) => {
          console.error('Error fetching user details:', error);
          // Handle error (e.g., redirect to login if unauthorized)
          this.$router.push({ name: 'Login' });
        });
    },
  },
};
</script>
