<template>
  <recipe-filters @update:selected="handleFilterChange"></recipe-filters>

  <div id="content">
    <div v-if="loading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>

    <v-row no-gutters v-if="recipesStore.currentPageRecipes.length">
      <v-col cols="12" sm="4" class="pa-2" v-for="recipe in recipesStore.currentPageRecipes" :key="recipe.recipe_id">
        <recipe-card
          :recipe_id="recipe.recipe_id"
          :name="recipe.name"
          :headline="recipe.headline"
          :image_url="recipe.image_url"
          :tags="recipe.tags"
        ></recipe-card>
      </v-col>
    </v-row>
    <v-row no-gutters class="mb-6">
      <v-col cols="12">
        <v-pagination
          v-model="currentPage"
          :length="recipesStore.totalPages"
          circle
        ></v-pagination>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { useRecipesStore } from '@/stores/recipes';
import RecipeFilters from '@/components/recipes/RecipeFilters.vue';
import RecipeCard from '@/components/recipes/RecipeCard.vue';

const route = useRoute();
const router = useRouter();
const recipesStore = useRecipesStore();

const loading = ref(false);
const error = ref(null);
const currentPage = ref(recipesStore.currentPage);

const fetchData = async (page) => {
  if (recipesStore.currentPage === page && recipesStore.currentPageRecipes.length > 0) {
    return; // Data for this page is already available, no need to refetch
  }
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get(`/recipes?page=${page}&page_size=12`);
    recipesStore.updateCurrentPageData(page, response.data.recipes, response.data.total_pages);
    window.scrollTo(0, 0);
  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const pageFromQuery = parseInt(route.query.page, 10) || 1;
  currentPage.value = pageFromQuery;
  fetchData(pageFromQuery);
});

watch(currentPage, (newPage) => {
  router.replace({ query: { ...route.query, page: newPage }}).catch(err => {});
  fetchData(newPage);
});

const filters = ref({
});

function handleFilterChange(selectedFilters) {
  filters.value = { ...filters.value, ...newFilters };
  fetchData();
}
</script>

<style scoped>
#content {
    max-width: 60vw;
    margin: auto;
}
</style>
