import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize auth store after pinia is set up
import { useAuthStore } from './store/auth'
const authStore = useAuthStore()
authStore.initFromStorage()

app.mount('#app')