<template>
    <div id="content" class="mb-4">
        <h1 class="mt-5 mb-8">Ajouter un aliment</h1>
        <v-stepper alt-labels v-model="step" :items="items" show-actions>
            <template v-slot:item.1>
                <food-description-form></food-description-form>
            </template>

            <template v-slot:item.2>
                <food-portions-form @snackbar="handleSnackbar"></food-portions-form>
            </template>

            <template v-slot:prev>
                <v-btn @click="prev">Précédent</v-btn>
            </template>
            <template v-slot:next>
                <v-btn v-if="!isFinalStep" @click="next">Suivant</v-btn>
                <v-btn v-else @click="next" :disabled="false" color="green">Ajouter l'aliment'</v-btn>
            </template>
        </v-stepper>

        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout" min-width="0">
                {{ snackbarMessage }}
        </v-snackbar>

    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

import FoodDescriptionForm from '../components/foods/FoodDescriptionForm.vue';
import FoodPortionsForm from '../components/foods/FoodPortionsForm.vue';

const step = ref(1);
const items = ref([
    'Description',
    'Portions'
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
}

function next() {
    if (step.value < items.value.length) {
        step.value++;
    }
}

function handleSnackbar({ message, color }) {
    snackbarMessage.value = message;
    snackbarColor.value = color;
    snackbar.value = true;
}

</script>


<style scoped>
h1 {
    text-align: center;
    font-size: 2rem;
    font-weight: 500;
    line-height: 1.6;
    letter-spacing: 0.0075em;
}

#content {
    max-width: 60vw;
    margin: auto;
}

#snackbar {
    text-align: center;
}
</style>
