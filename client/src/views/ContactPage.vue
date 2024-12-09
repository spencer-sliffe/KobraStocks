<!-- Prologue
Component Name: ContactPage
Path: src/views/ContactPage.vue

Description:
Provides a contact form for users to reach out with questions or messages, including fields for name, email, and message content.
-->

<template>
  <div>
    <div class="main-content">
      <h2>Contact Us</h2>
      <p>If you have any questions, please feel free to reach out to us:</p>
      <p>Email: info@kobrastocks.com</p>
      <p>Phone: +123 456 7890</p>
      <form @submit.prevent="sendMessage">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" required />

        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />

        <label for="message">Message:</label>
        <textarea id="message" v-model="message" required></textarea>

        <button type="submit">Send Message</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ContactPage',
  data() {
    return {
      name: '',
      email: '',
      message: '',
    };
  },
  methods: {
    sendMessage() {
      const contactData = {
        name: this.name,
        email: this.email,
        message: this.message,
      };

      axios
        .post('/api/contact', contactData)
        .then(() => {
          alert('Message sent successfully!');
          // Clear the form fields
          this.name = '';
          this.email = '';
          this.message = '';
        })
        .catch((error) => {
          console.error('Error sending message:', error);
          alert('Failed to send message. Please try again later.');
        });
    },
  },
};
</script>
