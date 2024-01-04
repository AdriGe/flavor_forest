<template>
    <recipe-filters></recipe-filters>

    <div id="content">
        <v-row no-gutters>
            <v-col cols="12" sm="4" class="pa-2" v-for="recipe in recipes" :key="recipe.id" :recipe="recipe">
                <recipe-card></recipe-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import { ref, watch } from 'vue';
import RecipeFilters from '../components/recipes/RecipeFilters.vue';
import RecipeCard from '../components/recipes/RecipeCard.vue';
import RecipeView from '../pages/RecipeView.vue';

export default {
    name: 'RecipesList',
    components: {
        RecipeFilters,
        RecipeCard,
        RecipeView,

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
