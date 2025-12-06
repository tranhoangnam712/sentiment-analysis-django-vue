import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server:{
	host:true,
	allowedHosts:['f91f9308e2af.ngrok-free.app', 'localhost'],
  },
})
