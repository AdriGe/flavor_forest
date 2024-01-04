<template>
        <v-row align="center">
            <v-spacer></v-spacer>
            <v-col cols="12" sm="4">
                <v-text-field label="Ingrédient" variant="underlined"></v-text-field>
            </v-col>
            <v-col cols="12" sm="2">
                <v-text-field label="Quantité" variant="underlined"></v-text-field>
            </v-col>
            <v-col cols="12" sm="3">
                <v-text-field label="Unité ou Portion" variant="underlined"></v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col cols="12" sm="1">
                <v-btn icon="mdi-delete" @click="onDeleteButtonClicked"></v-btn>
            </v-col>
        </v-row>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    id: {
        type: [String],
        required: true
    }
});

const emit = defineEmits(['update', 'delete']);


let content = ref('');

function onDeleteButtonClicked() {
    emit('delete', props.id);
}




</script>

<style scoped></style>