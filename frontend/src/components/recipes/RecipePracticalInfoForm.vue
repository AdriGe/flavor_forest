<template>
    <v-row>
        <v-col cols="12" sm="3" class="ml-3">
            <v-text-field variant="underlined" v-model="totalTime" :rules="rules" label="Temps total" type="number"
                min="0"></v-text-field>
        </v-col>
        <v-col cols="12" sm="3">
            <v-text-field variant="underlined" v-model="prepTime" :rules="rules" label="Temps de préparation" type="number"
                min="0"></v-text-field>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="5" class="mr-3" align="center">
            <label>Difficulté</label>
            <v-slider :ticks="difficulties" :max="2" step="1" show-ticks="always" tick-size="3" :color="color"
                v-model="difficulty"></v-slider>
        </v-col>
    </v-row>
    <v-row>
        <v-col cols="12" sm="4">
            <culinary-styles-tags></culinary-styles-tags>
        </v-col>
        <v-col cols="12" sm="4">
            <dietary-regime-tags></dietary-regime-tags>
        </v-col>
        <v-col cols="12" sm="4">
            <meal-type-tags></meal-type-tags>
        </v-col>
    </v-row>
    <v-divider></v-divider>
    <v-row>
        <v-col cols="12" sm="12">
            <add-usentils></add-usentils>
        </v-col>
    </v-row>
    <v-divider></v-divider>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';

import CulinaryStylesTags from './ui/tags/CulinaryStylesTags.vue';
import DietaryRegimeTags from './ui/tags/DietaryRegimeTags.vue';
import MealTypeTags from './ui/tags/MealTypeTags.vue';
import ImageUploadWithPreview from './ui/ImageUploadWithPreview.vue';
import AddUsentils from './ui/AddUstentils.vue';

let totalTime = ref(null);
let prepTime = ref(null);
let difficulty = ref(0);
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
