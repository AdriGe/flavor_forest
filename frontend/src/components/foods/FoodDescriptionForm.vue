<template>
    <v-row align="center">
        <v-col cols="12" sm="8" class="mt-3 mb-5">
            <v-text-field variant="underlined" v-model="name" :rules="rules" label="Nom de l'aliment"></v-text-field>
            <v-text-field variant="underlined" v-model="brand" :rules="rules" label="Marque (optionnel)"></v-text-field>
            <food-unit-picker></food-unit-picker>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="4" class="d-flex">
            <v-spacer></v-spacer>
            <div>
                <image-upload-with-preview></image-upload-with-preview>
            </div>
        </v-col>
    </v-row>
    <v-divider class="mb-2"></v-divider>
    <h2>Valeurs nutritionnelles (pour 100g)</h2>
    <v-row class="mt-3">
        <v-col cols="12" sm="12">
            <v-row>
                <v-col cols="12" sm="12">
                    <v-text-field variant="underlined" density="compact" v-model="calories" :rules="rules" type="number" min="0"
                step="0" label="Calories"></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="6">
                    <v-text-field variant="underlined" density="compact" v-model="fats" :rules="rules" type="number" min="0"
                step="0.1" label="Graisses"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-text-field variant="underlined" density="compact" v-model="saturated_fats" :rules="rules" type="number"
                min="0" step="0.1" label="Dont graisses saturées"></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="6">
                    <v-text-field variant="underlined" density="compact" v-model="carbohydrates" :rules="rules" type="number"
                min="0" step="0.1" label="Glucides"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-text-field variant="underlined" density="compact" v-model="sugars" :rules="rules" type="number" min="0"
                step="0.1" label="Dont sucre"></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="4">
                    <v-text-field variant="underlined" density="compact" v-model="fibers" :rules="rules" type="number" min="0"
                step="0.1" label="Fibres"></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                    <v-text-field variant="underlined" density="compact" v-model="proteins" :rules="rules" type="number" min="0"
                step="0.1" label="Protéines"></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                    <v-text-field variant="underlined" density="compact" v-model="sodium" :rules="rules" type="number" min="0"
                step="0.1" label="Sel"></v-text-field>
                </v-col>
            </v-row>









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
