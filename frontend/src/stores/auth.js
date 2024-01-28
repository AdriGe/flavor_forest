// store/auth.js
import { defineStore } from 'pinia';
import api from '@/services/api'; 

export const useAuthStore = defineStore('auth', {
    state: () => ({
        // Pas besoin de stocker le token ici, on le récupère directement du localStorage
    }),
    getters: {
        accessToken: () => {
            const token = localStorage.getItem('access_token');
            if (token) {
                // Vérifiez ici si le token est expiré
                return token;
            }
            return null;
        },
    },
    actions: {
        async refreshToken() {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const response = await api.post('/users/refresh-token', { refresh_token: refreshToken });
                    localStorage.setItem('access_token', response.data.access_token);
                } catch (error) {
                    // Gérez l'erreur, par exemple déconnectez l'utilisateur
                }
            }
        },
    },
});
