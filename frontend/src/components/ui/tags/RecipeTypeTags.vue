
<template>
    <v-select density="compact" clearable chips label="Type de cuisine" :items="recipeTypes" multiple></v-select>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const recipeTypes = ref([
            "Asiatique",
            "Américaine",
            "Italienne",
            "Française",
            "Méditerranéenne",
            "Indienne",
            "Mexicaine",
            "Chinoise",
            "Japonaise",
            "Thaïlandaise",
            "Africaine",
            "Caraïbéenne",
            "Moyen-Orientale",
            "Latino-Américaine",
            "Vietnamienne",
            "Espagnole",
            "Grecque",
            "Scandinave"
        ]);

        return {
            recipeTypes
        };
    }
};
</script>
