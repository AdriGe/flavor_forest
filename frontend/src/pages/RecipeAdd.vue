<template>
    <div id="content">
        <h1>Ajouter une recette</h1>
        <v-form @submit.prevent>
            <v-row>
                <v-col cols="12" sm="3" class="align-self-center">
                    <v-file-input prepend-icon="mdi-camera" label="Image d'illustration"></v-file-input>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field v-model="title" :rules="rules" label="Titre de la recette"></v-text-field>
                    <v-text-field v-model="subtitle" :rules="rules" label="Sous titre"></v-text-field>
                </v-col>
            </v-row>

            <v-textarea label="Description"></v-textarea>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-text-field v-model="totalTime" :rules="rules" label="Temps total" type="number" min="0"></v-text-field>
                </v-col>
                <v-col cols="12" sm="3">
                    <v-text-field v-model="prepTime" :rules="rules" label="Temps de préparation" type="number" min="0"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-select label="Difficulté" :items="['Facile', 'Intermédiaire', 'Difficile']"></v-select>
                </v-col>
            </v-row>

            <v-btn type="submit" block class="mt-2">Submit</v-btn>
        </v-form>
        <!--
        <v-row class="mt-2">
            <v-col cols="12" sm="10">
            </v-col>
            <v-col cols="12" sm="2" class="align-self-center">
            </v-col>
        </v-row>
        -->
    </div>
</template>

<script>
import { ref, watch } from 'vue';
import RecipeFilters from '../components/RecipeFilters.vue';
import RecipeCard from '../components/RecipeCard.vue';
import RecipeView from '../pages/RecipeView.vue';

export default {
    name: 'RecipesList',
    components: {
        RecipeFilters,
        RecipeCard,
        RecipeView
    },
    setup() {
        const recipes = ref([
            { id: 1, title: 'Recipe 1' },
            { id: 2, title: 'Recipe 2' },
            { id: 3, title: 'Recipe 3' },
            { id: 4, title: 'Recipe 4' },
            { id: 5, title: 'Recipe 5' },
            { id: 6, title: 'Recipe 6' },
            { id: 7, title: 'Recipe 7' },
            { id: 8, title: 'Recipe 8' },
            { id: 9, title: 'Recipe 9' },
            { id: 10, title: 'Recipe 10' }
        ]);

        return {
            recipes
        };
    }
};
</script>

<style scoped>
#content {
    max-width: 60vw;
    margin: auto;
}
</style>
