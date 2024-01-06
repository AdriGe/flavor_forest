<template>
    <v-sheet class="pa-12" rounded>
        <v-card class="mx-auto px-6 py-8" max-width="344px">
            <h2>Connexion</h2>
            <br>
            <v-form v-model="form" @submit.prevent="onSubmit">
                <v-text-field variant="outlined" v-model="email" :readonly="loading" :rules="[required]" class="mb-2" clearable
                    label="Email"></v-text-field>

                <v-text-field variant="outlined" v-model="password" :readonly="loading" :rules="[required]" clearable label="Mot de passe"
                    placeholder="Entrer votre mot de passe"></v-text-field>

                <br>

                <v-btn :disabled="!form" :loading="loading" block color="success" size="large" type="submit"
                    variant="elevated">
                    Connexion
                </v-btn>
            </v-form>
        </v-card>
    </v-sheet>
</template>

<script setup>
import { ref } from 'vue';


let form = ref(false);
let email = ref(null);
let password = ref(null);
let loading = ref(false);


function onSubmit() {
    if (!this.form) return

    loading.value = true

    setTimeout(() => (loading.value = false), 2000)
}

function required(v) {
    return !!v || 'Ce champ est requis'
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
