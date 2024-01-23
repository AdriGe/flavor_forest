<template>
    <v-app-bar>
        <v-row align="center" no-gutters>
            <v-spacer></v-spacer>
            <v-col cols="10" sm="6">
                <v-text-field rounded density="compact" variant="outlined" clearable :value="selectedFilters.searchText"
                    @input="handleSearchTextChange" label="Rechercher une recette" hide-details="true">
                    <template v-slot:append>
                        <v-btn icon="mdi-magnify"></v-btn>
                        <v-btn prepend-icon="mdi-filter-variant" @click="handleAppBarExtended">Filtrer</v-btn>
                    </template>

                </v-text-field>
            </v-col>
            <v-col cols="10" sm="2" class="d-flex">
                <v-spacer />
                <router-link to="/recipes/add">
                    <v-btn prepend-icon="mdi-plus" variant="outlined" rounded color="green">Ajouter</v-btn>
                </router-link>
            </v-col>
            <v-spacer></v-spacer>
        </v-row>
        <template v-if="isAppBarExtended" v-slot:extension>
            <v-row align="center" class="mt-6" no-gutters>
                <v-spacer></v-spacer>
                <v-col cols="10" sm="2" class="pr-2">
                    <culinary-styles-tags :max-elements="1" @update:selected="handleCulinaryStyleUpdate"></culinary-styles-tags>
                </v-col>
                <v-col cols="10" sm="2" class="pr-2">
                    <dietary-regime-tags :max-elements="1" @update:selected="handleDietaryRegimeUpdate"></dietary-regime-tags>
                </v-col>
                <v-col cols="10" sm="2" class="pr-2">
                    <meal-type-tags :max-elements="1" @update:selected="handleMealTypeUpdate"></meal-type-tags>
                </v-col>
                <v-col cols="10" sm="2">
                    <total-time-tags @update:selected="handleTotalTimeUpdate"></total-time-tags>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
        </template>
    </v-app-bar>
</template>

<script setup>
import { ref, watch } from 'vue';
import CulinaryStylesTags from './ui/tags/CulinaryStylesTags.vue';
import DietaryRegimeTags from './ui/tags/DietaryRegimeTags.vue';
import MealTypeTags from './ui/tags/MealTypeTags.vue';
import TotalTimeTags from './ui/tags/TotalTimeTags.vue';

let isAppBarExtended = ref(false);
function handleAppBarExtended() {
    isAppBarExtended.value = !isAppBarExtended.value;

}
const emit = defineEmits(['update:selected']);

let selectedFilters = ref({
    searchText: '',
    culinaryStyles: [],
    dietaryRegimes: [],
    mealTypes: [],
    totalTime: null
});

const handleSearchTextChange = (event) => {
    selectedFilters.value = { ...selectedFilters.value, searchText: event.target.value };
};

function handleMealTypeUpdate(selected) {
    selectedFilters.value = { ...selectedFilters.value, mealTypes: selected };
}

function handleDietaryRegimeUpdate(selected) {
    selectedFilters.value = { ...selectedFilters.value, dietaryRegimes: selected };
}

function handleCulinaryStyleUpdate(selected) {
    selectedFilters.value = { ...selectedFilters.value, culinaryStyles: selected };
}

function handleTotalTimeUpdate(selected) {
    selectedFilters.value = { ...selectedFilters.value, totalTime: selected };
}

watch(selectedFilters, (newSelectedFilters) => {
    emit('update:selected', newSelectedFilters);
});


</script>
