<template>
  <div class="footer-wrapper">
    <div class="footer-content">
      <!-- Left: Copyright -->
      <div class="text-medium-emphasis text-center text-md-left">
        &copy; {{ new Date().getFullYear() }}
        <span class="text-primary fw-bold">Daliso Rumbi Miti</span>
        <span class="d-none d-md-inline"> — Built with
          <VIcon icon="ri-heart-fill" color="error" size="0.9rem" />
          for elephant conservation
        </span>
      </div>

      <!-- Right: Social links -->
      <div class="social-links">
        <a
          href="https://github.com/PinkLemo/elephant-habitat"
          target="_blank"
          rel="noopener noreferrer"
          class="social-link"
          title="GitHub Repository"
        >
          <VIcon icon="ri-github-fill" size="1.3rem" />
        </a>
        <a
          href="https://www.linkedin.com/in/daliso-miti-805b8323a/"
          target="_blank"
          rel="noopener noreferrer"
          class="social-link"
          title="LinkedIn"
        >
          <VIcon icon="ri-linkedin-box-fill" size="1.3rem" />
        </a>
        <a
          href="mailto:dalisomiti@gmail.com"
          class="social-link"
          title="Email"
        >
          <VIcon icon="ri-mail-fill" size="1.3rem" />
        </a>
        <a
          href="https://my-portfolio-vue-steel.vercel.app/"
          target="_blank"
          rel="noopener noreferrer"
          class="social-link"
          title="Portfolio Website"
        >
          <VIcon icon="ri-global-line" size="1.3rem" />
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.footer-wrapper {
  width: 100%;
  padding: 1rem 0;
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.footer-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.text-primary {
  color: rgb(var(--v-theme-primary)) !important;
}

.fw-bold {
  font-weight: 600;
}

.social-links {
  display: flex;
  gap: 1.25rem;
  align-items: center;
}

.social-link {
  color: rgba(var(--v-theme-on-surface), 0.6);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}

.social-link:hover {
  color: rgb(var(--v-theme-primary));
  transform: translateY(-2px);
}

.social-link:active {
  transform: translateY(0);
}

@media (max-width: 600px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .social-links {
    gap: 1rem;
  }
}
</style>
