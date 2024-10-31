<template>
  <div>
    <h1>Account Details</h1>
    <div v-if="user">
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>First Name:</strong> {{ user.first_name }}</p>
      <p><strong>Last Name:</strong> {{ user.last_name }}</p>
      <p><strong>Phone Number:</strong> {{ user.phone_number }}</p>

      <!-- Budget Section -->
      <div>
        <label for="budget"><strong>Budget:</strong></label>
        <input
            type="number"
            id="budget"
            v-model.number="budget"
            step="0.01"
            min="0"
        />
        <button @click="updateBudget">Update Budget</button>
      </div>
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
      budget: null,
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
            this.budget = this.user.budget;
          })
          .catch((error) => {
            console.error('Error fetching user details:', error);
            this.$router.push({name: 'Login'});
          });
    },
    updateBudget() {
      axios
          .put('/api/user/budget', {budget: this.budget})
          .then(() => {
            alert('Budget updated successfully!');
          })
          .catch((error) => {
            console.error('Error updating budget:', error);
            alert('Failed to update budget. Please try again.');
          });
    },
  },
};
</script>
