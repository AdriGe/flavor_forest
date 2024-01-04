<template>
    <div id="content" class="mb-4">
        <h1>Ajouter une recette</h1>
        <v-form @submit.prevent>
            <v-row class="mb-3">
                <v-col cols="12" sm="8">
                    <v-text-field variant="underlined" v-model="title" :rules="rules"
                        label="Titre de la recette"></v-text-field>
                    <v-text-field variant="underlined" v-model="subtitle" :rules="rules" label="Sous titre"></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                    <v-spacer></v-spacer>
                    <image-upload-with-preview width="150" height="150"></image-upload-with-preview>
                </v-col>
            </v-row>



            <v-textarea variant="outlined" label="Description"></v-textarea>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-text-field variant="underlined" v-model="totalTime" :rules="rules" label="Temps total" type="number"
                        min="0"></v-text-field>
                </v-col>
                <v-col cols="12" sm="3">
                    <v-text-field variant="underlined" v-model="prepTime" :rules="rules" label="Temps de préparation"
                        type="number" min="0"></v-text-field>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="12" sm="4">
                    <v-slider :ticks="difficulties" :max="2" step="1" show-ticks="always" tick-size="3" :color="color"
                        v-model="difficulty"></v-slider>
                </v-col>
            </v-row>

            <v-row class="mb-3">
                <v-col cols="12" sm="6">
                    <h2>Etapes</h2>
                </v-col>
                <v-col cols="12" sm="6" class="d-flex">
                    <v-spacer></v-spacer>
                    <v-btn prepend-icon="mdi-plus" variant="outlined" rounded color="green" @click="addStep">Ajouter une
                        étape</v-btn>
                </v-col>
            </v-row>
            <create-step v-for="step in steps" :key="step.id" :step-number="step.stepNumber" :id="step.id" class="mb-2"
                @delete="handleDeleteStep"></create-step>
            <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout">{{ snackbarMessage }}</v-snackbar>
            <v-btn block rounded color="green">Ajouter la recette</v-btn>
        </v-form>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import RecipeFilters from '../components/RecipeFilters.vue';
import RecipeTypeTags from '../components/ui/tags/RecipeTypeTags.vue';
import DietaryRegimeTags from '../components/ui/tags/DietaryRegimeTags.vue';
import ImageUploadWithPreview from '../components/ui/ImageUploadWithPreview.vue';
import CreateStep from '../components/ui/CreateStep.vue';

let title = ref('');
let subtitle = ref('');
let totalTime = ref(0);
let prepTime = ref(0);
let difficulty = ref(0);
let rules = ref([]);
let steps = ref([
    { id: self.crypto.randomUUID(), stepNumber: 1 }
]);
let snackbar = ref(false);
let snackbarMessage = ref('');
let snackbarTimeout = ref(5000);
let snackbarColor = ref('gray');

const color = computed(() => {
    if (difficulty.value == 0) return 'green'
    if (difficulty.value == 1) return 'orange'
    if (difficulty.value == 2) return 'red'
});

const addStep = () => {
    steps.value.push({ id: self.crypto.randomUUID(), stepNumber: steps.value.length + 1 });
}

function handleDeleteStep(stepNumber) {
    if (steps.value.length == 1) {
        snackbarMessage.value = 'Au moins une étape est nécessaire';
        snackbarColor.value = 'red';
        snackbar.value = true;
        return
    };
    steps.value = steps.value.filter(step => step.id != stepNumber);
    steps.value.forEach((step, index) => {
        step.stepNumber = index + 1;
    });
}


let difficulties = ref({
    0: 'Facile',
    1: 'Intermédiaire',
    2: 'Difficile'
});
</script>


<style scoped>
#content {
    max-width: 60vw;
    margin: auto;
}
</style>
