<template>

<recipe-filters></recipe-filters>
    <div v-if="loading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>
    <div v-if="recipe">
        <v-card class="mx-auto my-8" max-width="60vw" elevation="16">
            <v-parallax gradient="to bottom, rgba(0,0,0,0), rgba(0,0,0,0), rgba(0,0,0,.33), rgba(0,0,0,.7)"
                class="align-end text-white" :src="'/src/assets/images/recipes/'+recipe.image_url" :scale="0.9" height="45vh">
                <v-card-item>
                    <v-card-title id="recipeTitle">
                        {{ recipe.name }}
                    </v-card-title>
                    <v-card-subtitle id="recipeSubtitle">
                        {{ recipe.headline }}
                    </v-card-subtitle>
                </v-card-item>
            </v-parallax>
            <v-card-item>
                <v-row no-gutters class="ma-2">
                    <v-col cols="12" sm="3">
                        <span class="basic-info-header">Temps total</span>
                        <span class="basic-info-value">{{ recipe.total_time }} minutes</span>
                    </v-col>
                    <v-col cols="12" sm="3">
                        <span class="basic-info-header">Calories</span>
                        <span class="basic-info-value">{{ recipe.kcal }} kcal</span>
                    </v-col>
                    <v-col cols="12" sm="3">
                        <span class="basic-info-header">Difficulté</span>
                        <span class="basic-info-value">{{ getDifficultyString(recipe.difficulty) }}</span>
                    </v-col>
                </v-row>
            </v-card-item>
            <v-divider></v-divider>



            <v-card-item>
                <v-chip v-for="tag in recipe.tags" :key="tag.tag_id" :color="getTagColor(tag.name)" class="mr-2 mt-2">
                    {{ tag.name }}
                </v-chip>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Description</h2>
                <span>
                    {{ recipe.description }}
                </span>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Ingrédients</h2>
                <v-row no-gutters class="ma-2">
                    <v-col v-for="food in recipe.foods" :key="food.food_id" cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img :src="'/src/assets/images/recipes/'+food.image_url" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">{{ food.quantity }} {{ food.unit}}</span>
                                <span class="food-name">{{ food.food_name }}</span>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <span></span>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item class="pa-5">
                <h2>Ustensiles</h2>
                <span>
                    <ul class="horizontal-list">
                        <li v-for="utensil in recipe.utensils" :key="utensil">{{ utensil }}</li>
                    </ul>
                </span>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Instructions</h2>
                <v-row v-for="(step, index) in recipe.steps" :key="'step_'+index" no-gutters class="mb-3">
                    <v-col cols="12" sm="4">
                        <v-img :src="'/src/assets/images/steps/'+recipe.steps_images_url[index]+'.jpg'">
                            <div class="step-number-box">
                                <div class="step-number">{{ index+1 }}</div>
                            </div>
                        </v-img>
                    </v-col>
                    <v-col cols="12" sm="8" class="pl-10 align-self-center">
                        <ul>
                            <li>{{ step }}</li>
                        </ul>
                    </v-col>
                </v-row>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Valeurs nutritionnelles</h2>
                <v-data-table :items="items" :headers="headers" density="compact" :hover="true" :items-per-page="99">
                    <template v-slot:header.nutrient="{ column }">
                        <span class="nutritional-facts-header">
                            {{ column.title }}
                        </span>
                    </template>
                    <template v-slot:header.perPortion="{ column }">
                        <span class="nutritional-facts-header">
                            {{ column.title }}
                        </span>
                    </template>
                    <template v-slot:header.per100g="{ column }">
                        <span class="nutritional-facts-header">
                            {{ column.title }}
                        </span>
                    </template>
                    <template v-slot:bottom></template>
                </v-data-table>
            </v-card-item>
        </v-card>
    </div>
</template>

<script setup>

import { ref, onMounted, watch } from 'vue';
import { useRecipesStore } from '@/stores/recipes';
import { useRoute } from 'vue-router';
import api from '@/services/api';
import RecipeFilters from '../components/recipes/RecipeFilters.vue';

const route = useRoute();
const recipesStore = useRecipesStore();
const recipeId = route.params.recipe_id;
const recipe = ref(null);
const error = ref(null);
const loading = ref(false);

const fetchRecipe = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get(`/recipes/${recipeId}`);
    recipesStore.addRecipe(response.data);
    recipe.value = response.data;
  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  if (recipesStore.recipes[recipeId.value]) {
    recipe.value = recipesStore.recipes[recipeId.value];
  } else {
    await fetchRecipe(recipeId.value);
  }
});

watch(route, async (newRoute) => {
  recipeId.value = newRoute.params.recipe_id;
  if (recipesStore.recipes[recipeId.value]) {
    recipe.value = recipesStore.recipes[recipeId.value];
  } else {
    await fetchRecipe(recipeId.value);
  }
});

const getDifficultyString = (difficultyInt) => {
    // Define logic to determine the color of the tag based on its value
    // Example:
    switch (difficultyInt) {
        // Dietary Regime
        case 1: return 'Facile'; // Darker Green
        case 2: return 'Intermédiaire'; // Sea Green
        case 3: return 'Difficile'; // Dark Goldenrod
        default: return '-'; // Black
    }
};

const getTagColor = (tag) => {
    // Define logic to determine the color of the tag based on its value
    // Example:
    switch (tag) {
        // Dietary Regime
        case 'Végétarien': return '#004d00'; // Darker Green
        case 'Vegan': return '#2e8b57'; // Sea Green
        case 'Sans gluten': return '#996515'; // Dark Goldenrod
        case 'Cétogène': return '#00008b'; // Dark Blue
        case 'Paleo': return '#654321'; // Darker Brown
        case 'Faible en glucides': return '#daa520'; // Goldenrod
        case 'Faible en calories': return '#4682b4'; // Steel Blue
        case 'Riche en protéines': return '#8b0000'; // Dark Red
        case 'Riche en légumes': return '#228b22'; // Forest Green
        case 'Détox': return '#3cb371'; // Medium Sea Green
        case 'Pescétarien': return '#00008b'; // Dark Blue
        case 'Flexitarien': return '#ff4500'; // Orange Red

        // Meal Type
        case 'Entrée': return '#4b0082'; // Indigo
        case 'Plat Principal': return '#800000'; // Maroon
        case 'Dessert': return '#db7093'; // Pale Violet Red
        case 'Amuse-bouche': return '#e9967a'; // Dark Salmon
        case 'Accompagnement': return '#696969'; // Dim Gray
        case 'Soupe': return '#6a5acd'; // Slate Blue
        case 'Salade': return '#2e8b57'; // Sea Green
        case 'Apéritif': return '#8b0000'; // Dark Red
        case 'Snack': return '#b8860b'; // Dark Goldenrod
        case 'Boisson': return '#20b2aa'; // Light Sea Green

        // Culinary Style
        case 'Turc': return '#8b4513'; // Saddle Brown
        case 'Vietnamienne': return '#556b2f'; // Dark Olive Green
        case 'Français': return '#00008b'; // Dark Blue
        case 'Britannique': return '#8b0000'; // Dark Red
        case 'Japonais': return '#8b0000'; // Dark Red
        case 'Moyen-Orient': return '#8b4513'; // Saddle Brown
        case 'Libanaise': return '#556b2f'; // Dark Olive Green
        case 'Chinois': return '#8b0000'; // Dark Red
        case 'Mexicain': return '#8b0000'; // Dark Red
        case 'Indien': return '#b8860b'; // Dark Goldenrod
        case 'Européen': return '#00008b'; // Dark Blue
        case 'Asiatique': return '#8b008b'; // Dark Magenta
        case 'Africain': return '#daa520'; // Goldenrod
        case 'Internationale': return '#ff6347'; // Tomato
        case 'Italien': return '#006400'; // Dark Green
        case 'Grec': return '#00008b'; // Dark Blue
        case 'Espagnol': return '#8b0000'; // Dark Red
        case 'Méditerranéen': return '#00008b'; // Dark Blue
        case 'Scandinave': return '#1e90ff'; // Dodger Blue
        case 'Coréenne': return '#a52a2a'; // Brown
        case 'Marocain': return '#191970'; // Midnight Blue
        case 'Latino-Américaine': return '#228b22'; // Forest Green
        case 'Américain': return '#00008b'; // Dark Blue
        case 'Thaï': return '#ba55d3'; // Medium Orchid

        default: return '#404040'; // Darker Grey (default color)
    }
};


const items = [
    { nutrient: "Énergie (kcal)", perPortion: "797kcal", per100g: "281kcal" },
    { nutrient: "Matières grasses", perPortion: "42.1g", per100g: "14.82g" },
    { nutrient: "dont acides gras saturés", perPortion: "13.4g", per100g: "4.72g" },
    { nutrient: "Glucides", perPortion: "77.8g", per100g: "27.39g" },
    { nutrient: "dont sucres", perPortion: "10g", per100g: "3.52g" },
    { nutrient: "Protéines", perPortion: "20.3g", per100g: "7.15g" },
    { nutrient: "Sel", perPortion: "2.61g", per100g: "0.92g" }
]


const headers = [
    { title: 'Nutriments', value: 'nutrient' },
    { title: 'Par portion (284g)', value: 'perPortion' },
    { title: 'Pour 100g', value: 'per100g' }
]
</script>

<style scoped>
#recipeTitle {
    font-size: 2rem;
}

#recipeSubtitle {
    font-size: 1.1rem;
}

.basic-info-header {
    display: block;
    font-size: 1.1rem;
    font-weight: bold;
}

.food-quantity {
    font-weight: bold;
    display: block;
}

.food-name {
    font-style: italic;
}

.horizontal-list li {
    display: inline-block;
    margin-right: 3rem;
}

.step-number-box {
    background-color: rgba(100, 100, 100, 0.25);
    position: absolute;
    padding: 5px;
    border-bottom-right-radius: 5px;
}

.step-number {
    width: 25px;
    height: 25px;
    line-height: 25px;
    border-radius: 50%;
    border: solid 1px;
    text-align: center;
    display: block;
}

.nutritional-facts-header {
    font-weight: bold;
    font-size: 1rem;
}
</style>