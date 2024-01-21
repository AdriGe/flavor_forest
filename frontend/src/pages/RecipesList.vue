<template>
    <recipe-filters></recipe-filters>

    <div id="content">
        <div v-if="loading">Loading...</div>
        <div v-if="error">Error: {{ error.message }}</div>

        <v-row no-gutters v-if="data">
            <v-col cols="12" sm="4" class="pa-2" v-for="[recipeId, recipeInfo] in Object.entries(recipes)" :key="recipeId">
                <recipe-card
                    :recipe_id="recipeInfo.data.recipe_id"
                    :name="recipeInfo.data.name"
                    :headline="recipeInfo.data.headline"
                    :image_url="recipeInfo.data.image_url"
                    :tags="recipeInfo.data.tags"
                ></recipe-card>
            </v-col>
        </v-row>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api'; // Adjust the path according to your project structure
import { useRecipesStore } from '@/stores/recipes';
import RecipeFilters from '@/components/recipes/RecipeFilters.vue';
import RecipeCard from '@/components/recipes/RecipeCard.vue';

const data = ref(null);
const error = ref(null);
const loading = ref(false);
const recipesStore = useRecipesStore();

const recipes = computed(() => recipesStore.recipes);

const fetchData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get('/recipes?page_size=12');
    data.value = response.data;
    recipesStore.addRecipes(data.value.recipes);

  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
};



onMounted(() => {
  fetchData();
});

</script>

<style scoped>
#content {
    max-width: 60vw;
    margin: auto;
}
</style>
