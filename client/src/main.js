import * as bootstrap from 'bootstrap/dist/js/bootstrap.bundle';
import 'bootstrap/dist/css/bootstrap.css'


import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

// import './assets/main.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
