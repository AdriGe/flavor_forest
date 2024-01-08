<template>
    <v-row align="center">
        <v-col cols="12" sm="7" class="mb-5">
            <v-text-field variant="underlined" v-model="name" :rules="rules" label="Nom de l'aliment"></v-text-field>
            <v-text-field variant="underlined" v-model="brand" :rules="rules" label="Marque (optionnel)"></v-text-field>
            <food-unit-picker></food-unit-picker>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="4">
            <image-upload-with-preview></image-upload-with-preview>
        </v-col>
    </v-row>
    <v-divider class="mb-2"></v-divider>
    <h2>Valeurs nutritionnelles (pour 100g)</h2>
    <v-row class="mt-3">
        <v-col cols="12" sm="3">
            <v-text-field variant="underlined" v-model="calories" :rules="rules" type="number" min="0" step="0" label="Calories"></v-text-field>
            <v-text-field variant="underlined" v-model="fats" :rules="rules" type="number" min="0" step="0.1" label="Graisses"></v-text-field>
            <v-text-field variant="underlined" v-model="saturated_fats" :rules="rules" type="number" min="0" step="0.1" label="Graisses saturées"></v-text-field>
            <v-text-field variant="underlined" v-model="carbohydrates" :rules="rules" type="number" min="0" step="0.1" label="Glucides"></v-text-field>
            <v-text-field variant="underlined" v-model="sugars" :rules="rules" type="number" min="0" step="0.1" label="Sucre"></v-text-field>
            <v-text-field variant="underlined" v-model="fibers" :rules="rules" type="number" min="0" step="0.1" label="Fibres"></v-text-field>
            <v-text-field variant="underlined" v-model="proteins" :rules="rules" type="number" min="0" step="0.1" label="Protéines"></v-text-field>
            <v-text-field variant="underlined" v-model="sodium" :rules="rules" type="number" min="0" step="0.1" label="Sel"></v-text-field>

        </v-col>
    </v-row>
    <v-divider></v-divider>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';

import FoodUnitPicker from './FoodUnitPicker.vue';
import ImageUploadWithPreview from '../common/ui/ImageUploadWithPreview.vue';

let name = ref(null);
let brand = ref(null);

const calories = ref(null)
const fats = ref(null)
const saturated_fats = ref(null)
const carbohydrates = ref(null)
const sugars = ref(null)
const fibers = ref(null)
const proteins = ref(null)
const sodium = ref(null)

let rules = ref([]);

const color = computed(() => {
    if (difficulty.value == 0) return 'green'
    if (difficulty.value == 1) return 'orange'
    if (difficulty.value == 2) return 'red'
});

let difficulties = ref({
    0: 'Facile',
    1: 'Intermédiaire',
    2: 'Difficile'
});
</script>

<style scoped>
label {
    font-size: 1.1rem;
}
</style>
