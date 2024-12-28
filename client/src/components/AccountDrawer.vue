<!-- AccountDrawer.vue -->
<template>
  <transition name="slide">
    <div class="account-drawer" v-if="isVisible">
      <div class="drawer-header">
        <h2>Account Details</h2>
        <button @click="closeDrawer">Close</button>
      </div>
      <div class="drawer-content">
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
      <!-- Logout Button Always Visible at the Bottom -->
      <div class="drawer-footer">
        <button @click="logout" class="logout-button">Logout</button>
      </div>
    </div>
  </transition>
</template>

<script>
import axios from 'axios';
import { authState } from '@/auth';

export default {
  name: 'AccountDrawer',
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      user: null,
      budget: null,
    };
  },
  watch: {
    isVisible(newVal) {
      if (newVal) {
        this.fetchUserDetails();
      }
    },
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
          this.$router.push({ name: 'Login' });
        });
    },
    updateBudget() {
      axios
        .put('/api/user/budget', { budget: this.budget })
        .then(() => {
          alert('Budget updated successfully!');
        })
        .catch((error) => {
          console.error('Error updating budget:', error);
          alert('Failed to update budget. Please try again.');
        });
    },
    logout() {
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
      authState.isAuthenticated = false;
      this.$emit('close'); // Close the drawer
      this.$router.push({ name: 'Login' });
    },
    closeDrawer() {
      this.$emit('close');
    },
  },
};
</script>
