
<template>
    <v-select 
        rounded
        variant="underlined"
        clearable
        v-model="value" 
        :items="items" 
        label="Type de cuisine"
        density="compact" 
        multiple
    >
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
const value = ref([]);

</script>
