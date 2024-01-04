<template>
    <v-app-bar>
        <v-row align="center" no-gutters>
            <v-spacer></v-spacer>
            <v-col cols="10" sm="6">
                <v-text-field rounded density="compact" variant="outlined" v-model="searchText"
                    label="Rechercher une recette" hide-details="true">
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
            <v-row align="center" class="mt-4" no-gutters>
                <v-spacer></v-spacer>
                <v-col cols="10" sm="2" class="pr-2">
                    <culinary-styles-tags></culinary-styles-tags>
                </v-col>
                <v-col cols="10" sm="2" class="pr-2">
                    <dietary-regime-tags></dietary-regime-tags>
                </v-col>
                <v-col cols="10" sm="2" class="pr-2">
                    <meal-type-tags></meal-type-tags>
                </v-col>
                <v-col cols="10" sm="2">
                    <v-select rounded variant="outlined" density="compact" clearable label="Durée max"
                        :items="maxPrepTime"></v-select>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
        </template>
    </v-app-bar>
</template>

<script>
import { ref } from 'vue';
import CulinaryStylesTags from './ui/tags/CulinaryStylesTags.vue';
import DietaryRegimeTags from './ui/tags/DietaryRegimeTags.vue';
import MealTypeTags from './ui/tags/MealTypeTags.vue';

export default {
    name: 'MyComponent',
    components: {
        CulinaryStylesTags,
        DietaryRegimeTags,
        MealTypeTags
    },
    setup() {
        const maxPrepTime = ref([
            '15 minutes',
            '30 minutes',
            '45 minutes',
            '60 minutes',
        ]);

        let isAppBarExtended = ref(false);
        function handleAppBarExtended() {
            isAppBarExtended.value = !isAppBarExtended.value;
            console.log(isAppBarExtended.value);
        }

        return {
            maxPrepTime,
            isAppBarExtended,
            handleAppBarExtended
        };
    },
};
</script>
