<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useFamilyStore } from '@/stores/familyStore';

const router = useRouter();
const store = useFamilyStore();
const password = ref('');
const error = ref('');

function login() {
  if (store.login(password.value)) {
    router.push('/admin');
  } else {
    error.value = 'Invalid password';
  }
}
</script>

<template>
  <div class="login-container">
    <div class="card login-card">
      <h2 class="text-center mb-lg">Admin Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label class="form-label">Password</label>
          <input type="password" v-model="password" class="form-input" placeholder="Enter admin password" />
        </div>
        <div v-if="error" class="error-msg">{{ error }}</div>
        <button type="submit" class="btn btn-primary btn-lg w-full">Login</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: var(--color-bg);
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.text-center {
  text-align: center;
}

.mb-lg {
  margin-bottom: var(--spacing-lg);
}

.w-full {
  width: 100%;
}

.error-msg {
  color: var(--color-error);
  margin-bottom: var(--spacing-md);
  text-align: center;
}
</style>
