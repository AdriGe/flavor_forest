<template>
    <v-sheet class="pa-12" rounded>
        <v-card class="mx-auto px-6 py-8" max-width="344px">
            <h2>Connexion</h2>
            <br>
            <v-form v-model="form" @submit.prevent="onSubmit">
                <v-text-field variant="outlined" v-model="email" :readonly="loading" :rules="[required]" class="mb-2" clearable
                    label="Email"></v-text-field>

                <v-text-field variant="outlined" v-model="password" :readonly="loading" :rules="[required]" clearable label="Mot de passe"
                    placeholder="Entrer votre mot de passe" type="password"></v-text-field>

                <br>

                <v-btn :disabled="!form" :loading="loading" block color="success" size="large" type="submit"
                    variant="elevated">
                    Connexion
                </v-btn>
            </v-form>
        </v-card>
        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout" min-width="0">
                {{ snackbarMessage }}
        </v-snackbar>
    </v-sheet>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api'; // Importez votre instance Axios

const router = useRouter(); // Create a router instance

let form = ref(false);
let email = ref(null);
let password = ref(null);
let loading = ref(false);

let snackbar = ref(false);
let snackbarMessage = ref('');
let snackbarTimeout = ref(5000);
let snackbarColor = ref('gray');

function extractErrorMessage(error) {
    if (error.response && error.response.data) {
        if (typeof error.response.data.detail === 'string') {
            return error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
            return error.response.data.detail.join(', ');
        } else {
            return JSON.stringify(error.response.data);
        }
    }
    return 'An error occurred';
}

async function onSubmit() {
    if (!form.value) return;
    loading.value = true;

    let formData = new FormData();
    formData.append('username', email.value);
    formData.append('password', password.value);

    try {
        const response = await api.post('/users/login', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        // Stockez le token et redirigez l'utilisateur si nécessaire
        loading.value = false;
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);

        snackbarMessage.value = "Vous êtes maintenant connecté. Redirection en cours...";
        snackbarColor.value = 'green';
        snackbar.value = true;

        setTimeout(() => {
            router.push('/recipes');
        }, 2000);
    } catch (error) {
        console.log(error);
        snackbarMessage.value = extractErrorMessage(error);
        snackbarColor.value = 'red';
        snackbar.value = true;

        loading.value = false;
    }
}

function required(v) {
    return !!v || 'Ce champ est requis';
}

</script>

<style scoped>
h2 {
    font-size: 2rem;
    font-weight: 500;
    line-height: 1.6;
    letter-spacing: 0.0075em;
    margin: 0;
    padding: 0;
    text-align: center;
}
</style>
