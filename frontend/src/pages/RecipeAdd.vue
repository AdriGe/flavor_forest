<template>
    <div id="content" class="mb-4">
        <h1>Ajouter une recette</h1>

            <v-stepper alt-labels :items="['Description', 'Ingrédients', 'Etapes']">
                <template v-slot:item.1>
                    <recipes-add-step-one></recipes-add-step-one>
                </template>

                <template v-slot:item.2>
                    <recipes-add-step-two @snackbar="handleSnackbar"></recipes-add-step-two>
                </template>

                <template v-slot:item.3>
                    <recipes-add-step-three @snackbar="handleSnackbar"></recipes-add-step-three>
                </template>
            </v-stepper>

            <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout">{{ snackbarMessage
            }}</v-snackbar>
            <v-btn block rounded color="green">Ajouter la recette</v-btn>

    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';


import RecipesAddStepOne from '../components/recipes/RecipesAddStepOne.vue';
import RecipesAddStepTwo from '../components/recipes/RecipesAddStepTwo.vue';
import RecipesAddStepThree from '../components/recipes/RecipesAddStepThree.vue';

let snackbar = ref(false);
let snackbarMessage = ref('');
let snackbarTimeout = ref(5000);
let snackbarColor = ref('gray');

function handleSnackbar({ message, color }) {
    snackbarMessage.value = message;
    snackbarColor.value = color;
    snackbar.value = true;
}

</script>


<style scoped>
#content {
    max-width: 60vw;
    margin: auto;
}
</style>
