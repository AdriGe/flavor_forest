
<template>
    <v-select rounded variant="outlined" v-model="value" :items="items" label="Unité" density="compact">
    </v-select>
</template>

<script setup>
import { ref } from 'vue';

const items = ref([
    "gramme",
    "millilitre",
    "centilitre",
    "litre"
]);
const value = ref([]);

</script>
