
<template>
    <v-select rounded variant="outlined" density="compact" clearable label="Durée max" v-model="value" :items="items"></v-select>
</template>

<script setup>
import { ref, watch } from 'vue';

const emit = defineEmits(['update:selected']);

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

watch(value, (newValue) => {
  emit('update:selected', newValue);
});

</script>
