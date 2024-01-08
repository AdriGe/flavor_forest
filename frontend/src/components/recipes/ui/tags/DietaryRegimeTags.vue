
<template>
    <v-select rounded variant="underlined" clearable v-model="value" :items="items" label="Régime alimentaire" density="compact"
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
const value = ref([]);

</script>
