
<template>
    <v-select 
        rounded 
        variant="outlined" 
        density="compact" 
        clearable 
        chips 
        label="Type de cuisine" 
        :items="culinaryStyles" 
        multiple
    ></v-select>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const culinaryStyles = ref([
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
            culinaryStyles
        };
    }
};
</script>
