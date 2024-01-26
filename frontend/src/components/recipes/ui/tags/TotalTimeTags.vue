<template>
    <v-select 
        rounded
        variant="outlined"
        density="compact"
        clearable
        label="Durée max"
        v-model="value"
        :items="items">
    </v-select>
</template>

<script setup>
import { ref, watch } from 'vue';

// Define the props
const props = defineProps({
    maxElements: {
        type: Number,
        default: 2
    },
    initialValue: {
        type: Number,
        default: null
    }
});

// Use the prop

const items = ref([
    { title: '15 minutes', value: 15 },
    { title: '30 minutes', value: 30 },
    { title: '45 minutes', value: 45 },
    { title: '60 minutes', value: 60 },
]);

// Find the item with the matching value
const matchedItem = items.value.find(item => item.value === props.initialValue);

// Initialize value with the title of the matched item
const value = ref(matchedItem ? matchedItem.title : null);

const emit = defineEmits(['update:selected']);

watch(value, (newValue) => {
  emit('update:selected', newValue);
});
</script>
