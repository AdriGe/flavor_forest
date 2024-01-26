
<template>
    <v-select 
        rounded
        variant="outlined"
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
import { ref, watch } from 'vue';

const emit = defineEmits(['update:selected']);

const props = defineProps({
    maxElements: {
        type: Number,
        default: 2
    },
    initialValue: {
        type: Array,
        default: []
    }
});

const value = ref(props.initialValue);

const items = ref([
    "Africain",
    "Américain",
    "Asiatique",
    "Britannique",
    "Chinois",
    "Coréenne",
    "Espagnol",
    "Européen",
    "Français",
    "Grec",
    "Indien",
    "Internationale",
    "Italien",
    "Japonais",
    "Latino-Américaine",
    "Libanaise",
    "Marocain",
    "Méditerranéen",
    "Mexicain",
    "Moyen-Orient",
    "Scandinave",
    "Thaï",
    "Turc",
    "Végétarien",
    "Vietnamienne"
]);


watch(value, (newValue) => {
  emit('update:selected', newValue);
});

</script>
