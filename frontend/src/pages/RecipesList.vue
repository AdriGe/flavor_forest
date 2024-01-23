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

const constructQueryString = (filters) => {
  let queryParams = new URLSearchParams();

  queryParams.append('page_size', 12);

  // Add searchText if it exists
  if (filters.searchText) {
    queryParams.append('name', filters.searchText);
  }

  // Add tags from all arrays
  ['culinaryStyles', 'dietaryRegimes', 'mealTypes'].forEach(key => {
    if (filters[key] && filters[key].length) {
      filters[key].forEach(tag => queryParams.append('tags', tag));
    }
  });

  return queryParams.toString();
};

const lastUsedFilters = ref('');

const fetchData = async (page) => {
  const currentFiltersString = constructQueryString(filters.value);
  if (recipesStore.currentPage === page && lastUsedFilters.value === currentFiltersString) {
    return; // Data for this page with the same filters is already available, no need to refetch
  }

  lastUsedFilters.value = currentFiltersString;
  loading.value = true;
  error.value = null;

  try {
    const queryString = `${currentFiltersString}`;
    const response = await api.get(`/recipes?page=${page}&${queryString}`);
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
  searchText: '',
  culinaryStyles: [],
  dietaryRegimes: [],
  mealTypes: []
});

function handleFilterChange(newFilters) {
  filters.value = { ...filters.value, ...newFilters };
  currentPage.value = 1;
  fetchData(currentPage.value);
}
</script>

<style scoped>
#content {
    max-width: 60vw;
    margin: auto;
}
</style>
