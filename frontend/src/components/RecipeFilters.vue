<template>
    <div>
        <v-row>
            <v-col cols="12" sm="10" class="mt-6 pl-5">
                <v-text-field density="compact" v-model="searchText" :rules="rules" label="Rechercher"></v-text-field>
                <v-row>
                    <v-col cols="12" sm="4">
                        <recipe-type-tags></recipe-type-tags>
                    </v-col>
                    <v-col cols="12" sm="4">
                        <dietary-regime-tags></dietary-regime-tags>
                    </v-col>
                    <v-col cols="12" sm="4">
                        <v-select density="compact" clearable label="Durée max" :items="maxPrepTime"></v-select>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="12" sm="2" align="right" width="100" class="align-self-center pr-5">
                <v-btn icon="mdi-magnify" size="x-large" class="w-100" rounded="xl" stacked></v-btn>
            </v-col>

        </v-row>
    </div>
</template>

<script>
import { ref } from 'vue';
import RecipeTypeTags from './ui/tags/RecipeTypeTags.vue';
import DietaryRegimeTags from './ui/tags/DietaryRegimeTags.vue';

export default {
    name: 'MyComponent',
    components: {
        RecipeTypeTags,
        DietaryRegimeTags
    },
    setup() {
        const maxPrepTime = ref([
            '15 minutes',
            '30 minutes',
            '45 minutes',
            '60 minutes',
        ]);

        return {
            maxPrepTime
        };
    },
};
</script>
