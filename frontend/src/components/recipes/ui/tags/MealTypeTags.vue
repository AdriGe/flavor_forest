
<template>
    <v-select 
        rounded 
        variant="outlined" 
        density="compact" 
        clearable 
        chips 
        label="Type de plat" 
        :items="mealTypes" 
        multiple
    ></v-select>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const mealTypes = ref([
    "Entrée",
    "Plat Principal",
    "Dessert",
    "Apéritif",
    "Accompagnement",
    "Soupe",
    "Salade",
    "Snack",
    "Petit-déjeuner",
    "Boisson"
]
);

        return {
            mealTypes
        };
    }
};
</script>
