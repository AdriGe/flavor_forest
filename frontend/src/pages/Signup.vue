<template>
    <v-sheet class="pa-12" rounded>
        <v-card class="mx-auto px-6 py-8" max-width="500px">
            <h2>Inscription</h2>
            <br>
            <v-form v-model="form" @submit.prevent="onSubmit">
                <v-text-field variant="outlined" v-model="email" :error-messages="emailError" @blur="validateEmail"
                    :readonly="loading" :rules="[required]" class="mb-2" label="Email"></v-text-field>
                <br>

                <v-text-field variant="outlined" label="Nom d'utilisateur" v-model="username" :error-messages="usernameError"
                    @blur="validateUsername"></v-text-field>
                <br>
                <v-text-field variant="outlined" v-model="password"
                    :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" :type="showPassword ? 'text' : 'password'"
                    @click:append-inner="showPassword = !showPassword" :error-messages="passwordError" :readonly="loading"
                    :rules="[required]" label="Mot de passe" @input="validatePassword"
                    placeholder="Choisissez votre mot de passe"></v-text-field>
                <br>

                <v-text-field variant="outlined" v-model="passwordConfirmation"
                    :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" :type="showPassword ? 'text' : 'password'"
                    @click:append-inner="showPassword = !showPassword" :readonly="loading" :rules="[required]"
                    :error-messages="passwordConfirmationError" @blur="validatePasswordConfirmation"
                    label="Confirmation du mot de passe" placeholder="Validez votre mot de passe"></v-text-field>
                <br>

                <v-btn :disabled="!form" :loading="loading" block color="success" size="large" type="submit"
                    variant="elevated">
                    S'inscrire
                </v-btn>
            </v-form>
        </v-card>
        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout" min-width="0">
                {{ snackbarMessage }}
        </v-snackbar>
    </v-sheet>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/api';
import { useRouter } from 'vue-router';

let form = ref(false);
let email = ref(null);
let username = ref(null);
let password = ref(null);
let passwordConfirmation = ref(null);
let loading = ref(false);
const showPassword = ref(false);
const emailError = ref('');
const usernameError = ref('');
const passwordError = ref('');
const passwordConfirmationError = ref('');

const router = useRouter(); // Create a router instance

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

async function registerUser(userData) {
    try {
        const response = await api.post('/users/register', userData);
        snackbarMessage.value = "Inscription réussie! Redirection en cours...";
        snackbarColor.value = 'green';
        snackbar.value = true;

        setTimeout(() => {
            router.push('/login');
        }, 2000);
    } catch (error) {
        snackbarMessage.value = extractErrorMessage(error);
        snackbarColor.value = 'red';
        snackbar.value = true;
    }
}

async function onSubmit() {
    if (!form.value) return;
    
    loading.value = true;

    const userData = {
        email: email.value,
        username: username.value,
        password: password.value
    };

    await registerUser(userData);

    loading.value = false;
}

function required(v) {
    return !!v || 'Ce champ est requis'
}

const validateEmail = () => {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    emailError.value = emailRegex.test(email.value) ? '' : 'Adresse email invalide';
};

const validateUsername = () => {
    const minLength = 3;
    const usernameRegex = /^[a-zA-Z0-9_-]+$/; // Adjust regex based on your requirements
    usernameError.value = '';
    if (username.value.length < minLength) {
        usernameError.value = `Le nom d'utilisateur doit contenir au moins ${minLength} caractères`;
    } else if (!usernameRegex.test(username.value)) {
        usernameError.value = 'Le nom d\'utilisateur ne doit contenir que des lettres, des chiffres, des tirets et des underscores';
    }
};

const validatePassword = () => {
    const regex = {
        length: /.{8,}/,
        upper: /[A-Z]/,
        lower: /[a-z]/,
        number: /[0-9]/,
        special: /[^A-Za-z0-9]/
    };

    let errors = [];
    if (!regex.length.test(password.value)) errors.push("Au moins 8 caractères");
    if (!regex.upper.test(password.value)) errors.push("Au moins une majuscule");
    if (!regex.lower.test(password.value)) errors.push("Au moins une minuscule");
    if (!regex.number.test(password.value)) errors.push("Au moins un chiffre");
    if (!regex.special.test(password.value)) errors.push("Au moins un caractère spécial");

    passwordError.value = errors.join(", ");
};

function validatePasswordConfirmation() {
    if (password.value !== passwordConfirmation.value) {
        passwordConfirmationError.value = 'Les mots de passe ne correspondent pas';
    } else {
        passwordConfirmationError.value = '';
    }
};

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
