
<template>
    <v-select rounded variant="outlined" density="compact" clearable label="Durée max" :items="items"></v-select>
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
    '15 minutes',
    '30 minutes',
    '45 minutes',
    '60 minutes',
]);
const value = ref([]);

</script>
