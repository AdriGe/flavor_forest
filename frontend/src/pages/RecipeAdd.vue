<template>
    <div id="content" class="mb-4">
        <h1>Ajouter une recette</h1>
        <v-form @submit.prevent>
            <v-row>
                <v-col cols="12" sm="9">
                    <v-text-field variant="underlined" v-model="title" :rules="rules"
                        label="Titre de la recette"></v-text-field>
                    <v-text-field variant="underlined" v-model="subtitle" :rules="rules" label="Sous titre"></v-text-field>
                </v-col>

                <v-col cols="12" sm="3" class="align-self-center">
                </v-col>
            </v-row>

            <image-upload-with-preview></image-upload-with-preview>

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
                <v-col cols="12" sm="6">
                    <v-select variant="underlined" label="Difficulté"
                        :items="['Facile', 'Intermédiaire', 'Difficile']"></v-select>
                </v-col>
            </v-row>

            <v-btn type="submit" block class="mt-2">Ajouter la recette</v-btn>
        </v-form>

    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import RecipeFilters from '../components/RecipeFilters.vue';
import RecipeTypeTags from '../components/ui/tags/RecipeTypeTags.vue';
import DietaryRegimeTags from '../components/ui/tags/DietaryRegimeTags.vue';
import ImageUploadWithPreview from '../components/ui/tags/ImageUploadWithPreview.vue';

let title = ref('');
let subtitle = ref('');
let totalTime = ref(0);
let prepTime = ref(0);
let rules = ref([]);


</script>


<style scoped>
#content {
    max-width: 60vw;
    margin: auto;
}
</style>
