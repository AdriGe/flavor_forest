import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const baseURL = `${import.meta.env.VITE_API_BASE_URL}:${import.meta.env.VITE_API_PORT}`;

const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
    console.log('Intercepting request');
    const token = localStorage.getItem('access_token');
    if (token) {
        console.log('Adding token to request');
        config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('Request intercepted');
    return config;
}, (error) => {
    console.log('Error intercepting request');
    return Promise.reject(error);
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        console.log('Intercepting response');
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            console.log('Intercepted 401 error');
            originalRequest._retry = true;
            const authStore = useAuthStore();
            await authStore.refreshToken();
            return api(originalRequest);
        }
        console.log('Response intercepted');
        return Promise.reject(error);
    }
);

export default api;
