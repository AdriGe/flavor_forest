<template>
    <div id="content" class="mb-4">
        <h1>Ajouter une recette</h1>

        <v-stepper  alt-labels v-model="step" :items="items" show-actions>
            <template v-slot:item.1>
                <recipes-add-step-one></recipes-add-step-one>
            </template>

            <template v-slot:item.2>
                <recipes-add-step-two></recipes-add-step-two>
            </template>

            <template v-slot:item.3>
                <recipes-add-step-three></recipes-add-step-three>
            </template>
            <template v-slot:actions.prev>
                Prev
            </template>
            <template v-slot:prev>
                <v-btn @click="prev">Précédent</v-btn>
            </template>
            <template v-slot:next>
                <v-btn v-if="!isFinalStep" @click="next">Suivant</v-btn>
                <v-btn v-else @click="next" :disabled="false" color="green">Ajouter la recette</v-btn>
            </template>
        </v-stepper>

        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout">{{ snackbarMessage
        }}</v-snackbar>

    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';


import RecipesAddStepOne from '../components/recipes/RecipesAddStepOne.vue';
import RecipesAddStepTwo from '../components/recipes/RecipesAddStepTwo.vue';
import RecipesAddStepThree from '../components/recipes/RecipesAddStepThree.vue';


const shipping = ref(0);
const step = ref(1);
const items = ref([
    'Description',
    'Ingrédients',
    'Etapes',
]);

const isFinalStep = computed(() => step.value === items.value.length);

let snackbar = ref(false);
let snackbarMessage = ref('');
let snackbarTimeout = ref(5000);
let snackbarColor = ref('gray');

function prev() {
    if (step.value > 1) {
        step.value--;
    }
    console.log(step.value);
}

function next() {
    if (step.value < items.value.length) {
        step.value++;
    }
    console.log(step.value);
}

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
