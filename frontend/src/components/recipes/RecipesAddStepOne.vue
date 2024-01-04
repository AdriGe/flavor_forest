<template>
    <v-row class="mb-3">
        <v-col cols="12" sm="8">
            <v-text-field variant="underlined" v-model="title" :rules="rules" label="Titre de la recette"></v-text-field>
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
            <v-text-field variant="underlined" v-model="prepTime" :rules="rules" label="Temps de préparation" type="number"
                min="0"></v-text-field>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="4">
            <v-slider :ticks="difficulties" :max="2" step="1" show-ticks="always" tick-size="3" :color="color"
                v-model="difficulty"></v-slider>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';

import RecipeTypeTags from './ui/tags/RecipeTypeTags.vue';
import DietaryRegimeTags from './ui/tags/DietaryRegimeTags.vue';
import ImageUploadWithPreview from './ui/ImageUploadWithPreview.vue';

let title = ref('');
let subtitle = ref('');
let totalTime = ref(0);
let prepTime = ref(0);
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

<style scoped></style>
