// client/src/auth.js
import { reactive } from 'vue';

export const authState = reactive({
  isAuthenticated: !!localStorage.getItem('token'),
});
