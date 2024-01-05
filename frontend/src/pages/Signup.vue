<template>
    <v-sheet class="pa-12" rounded>
        <v-card class="mx-auto px-6 py-8" max-width="344">
            <v-form v-model="form" @submit.prevent="onSubmit">
                <v-text-field variant="outlined" v-model="email" :readonly="loading" :rules="[required]" class="mb-2"
                    clearable label="Email"></v-text-field>

                <v-text-field variant="outlined" v-model="password" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'" @click:append="showPassword = !showPassword"
                    :error-messages="passwordError" :readonly="loading" :rules="[required]" clearable label="Mot de passe"
                    @input="validatePassword" placeholder="Choisissez votre mot de passe"></v-text-field>
                <br>

                <v-text-field variant="outlined" v-model="passwordConfirmation"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword" :readonly="loading" :rules="[required]"
                    :error-messages="passwordConfirmationError" @blur="validatePasswordConfirmation" clearable
                    label="Confirmation du mot de passe" placeholder="Validez votre mot de passe"></v-text-field>
                <br>

                <v-btn :disabled="!form" :loading="loading" block color="success" size="large" type="submit"
                    variant="elevated">
                    S'inscrire
                </v-btn>
            </v-form>
        </v-card>
    </v-sheet>
</template>

<script setup>
import { ref, computed } from 'vue';


let form = ref(false);
let email = ref(null);
let password = ref(null);
let passwordConfirmation = ref(null);
let loading = ref(false);
const showPassword = ref(false);
const passwordError = ref('');
const passwordConfirmationError = ref('');

function onSubmit() {
    if (!this.form) return

    loading.value = true

    setTimeout(() => (loading.value = false), 2000)
}

function required(v) {
    return !!v || 'Ce champ est requis'
}

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

<style scoped></style>
