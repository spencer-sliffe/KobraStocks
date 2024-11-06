<template>
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/about">About</router-link></li>
        <li><router-link to="/services">Services</router-link></li>
        <li><router-link to="/contact">Contact</router-link></li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'Navbar'
  };
  </script>
  
  <style scoped>
  /* Your CSS styling for the Navbar */
  nav ul {
    list-style: none;
    display: flex;
    gap: 20px;
  }
  nav ul li {
    margin: 0;
  }
  nav ul li a {
    color: var(--text-color);
    text-decoration: none;
  }
  </style>
  