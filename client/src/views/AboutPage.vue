<!-- Prologue
Component Name: AboutPage
Path: src/views/AboutPage.vue

Description:
Provides an "About Us" section for the KobraStocks application, detailing the mission, vision, team, and values to build trust with users.
-->


<template>
  <div class="main-content">
    <h2>About Us</h2>
    <p>
      At Kobra Stocks, our mission is to empower individuals to make informed investment decisions by providing accurate and accessible stock market predictions.
    </p>
    <p>
      Our vision is to revolutionize the financial landscape by bridging the gap between technology and investing, ensuring everyone has the tools to succeed in the stock market.
    </p>
    <h3>Our Values</h3>
    <ul class="values-list">
      <li><strong>Accuracy:</strong> Leveraging advanced machine learning models to deliver reliable predictions.</li>
      <li><strong>Transparency:</strong> Clear and user-friendly visualizations to support investment decisions.</li>
      <li><strong>Innovation:</strong> Continuously improving our platform with cutting-edge technology.</li>
      <li><strong>Inclusivity:</strong> Making the stock market accessible to everyone, regardless of expertise.</li>
    </ul>
    <h3>Meet Our Team</h3>
    <p>
      The Kobra Stocks team is comprised of financial experts, data scientists, and technology enthusiasts united by a common goal: to simplify investing for everyone.
      With a shared passion for innovation, our team ensures the platform remains at the forefront of market prediction technologies.
    </p>
    <h3>Why Trust Us?</h3>
    <p>
      At Kobra Stocks, we prioritize user confidence through transparency, rigorous testing of our models, and continuous optimization. Our commitment to excellence is reflected in the platform's growing community of satisfied investors.
    </p>
  </div>
</template>

<script>
export default {
  name: "AboutPage",
};
</script>