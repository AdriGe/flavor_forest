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
                console.log('Access token found in localStorage');
                // Vérifiez ici si le token est expiré
                return token;
            }
            console.log('Access token not found in localStorage');
            return null;
        },
    },
    actions: {
        async refreshToken() {
            const refreshToken = localStorage.getItem('refresh_token');
            console.log('Refreshing token');
            if (refreshToken) {
                try {
                    console.log('Refreshing token with API');
                    const response = await api.post('/users/refresh-token', { refresh_token: refreshToken });
                    localStorage.setItem('access_token', response.data.access_token);
                } catch (error) {
                    console.error('Erreur lors du rafraîchissement du token:', error);
                    // Gérez l'erreur, par exemple déconnectez l'utilisateur
                }
            }
        },
    },
});
