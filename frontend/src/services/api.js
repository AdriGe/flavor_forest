import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const baseURL = `${import.meta.env.VITE_API_BASE_URL}:${import.meta.env.VITE_API_PORT}`;

const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
    const authStore = useAuthStore();
    const token = authStore.accessToken;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const authStore = useAuthStore();
            await authStore.refreshToken();
            return api(originalRequest);
        }
        return Promise.reject(error);
    }
);

export default api;
