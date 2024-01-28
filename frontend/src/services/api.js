import axios from 'axios';
import router from '@/router';
import { useAuthStore } from '@/stores/auth';

const baseURL = `${import.meta.env.VITE_API_BASE_URL}:${import.meta.env.VITE_API_PORT}`;

const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
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
        if (error.response.status === 401) {
            // Vérifiez si l'erreur provient de l'endpoint de rafraîchissement du token
            if (originalRequest.url === '/users/refresh-token') {
                localStorage.clear();
                router.push('/login');
                return Promise.reject(error);
            }

            if (!originalRequest._retry) {
                originalRequest._retry = true;
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    try {
                        const response = await api.post('/users/refresh-token', { refresh_token: refreshToken });
                        localStorage.setItem('access_token', response.data.access_token);
                        return api(originalRequest);
                    } catch (refreshError) {
                        localStorage.clear();
                        router.push('/login');
                        return Promise.reject(refreshError);
                    }
                } else {
                    localStorage.clear();
                    router.push('/login');
                    return Promise.reject(error);
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;
