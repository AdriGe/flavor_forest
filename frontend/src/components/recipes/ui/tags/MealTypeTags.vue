
<template>
    <v-select rounded variant="outlined" clearable v-model="value" :items="items" label="Type de plat" density="compact"
        multiple>
        <template v-slot:selection="{ item, index }">
            <v-chip v-if="index < maxElements">
                <span>{{ item.title }}</span>
            </v-chip>
            <span v-if="index === maxElements" class="text-grey text-caption align-self-center">
                (+{{ value.length - maxElements }} {{ value.length - maxElements === 1 ? 'autre' : 'autres' }})
            </span>
        </template>
    </v-select>
</template>

<script setup>
import { ref } from 'vue';


const props = defineProps({
    maxElements: {
        type: Number,
        default: 2
    }
});

const items = ref([
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
]);
const value = ref([]);

</script>
