
<template>
    <v-select 
        rounded 
        variant="outlined"
        density="compact" 
        clearable 
        chips 
        label="Régime alimentaire" 
        :items="dietaryRegimes"
        multiple
    ></v-select>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const dietaryRegimes = ref([
            "Végétarien",
            "Vegan",
            "Sans gluten",
            "Cétogène",
            "Paleo",
            "Faible en glucides",
            "Faible en calories",
            "Riche en protéines",
            "Riche en légumes",
            "Détox",
            "Pescétarien",
            "Flexitarien"
        ]);

        return {
            dietaryRegimes
        };
    }
};
</script>
