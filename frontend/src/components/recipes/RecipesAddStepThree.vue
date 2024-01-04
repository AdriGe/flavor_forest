<template>
    <v-row class="my-3">
        <v-col cols="12" sm="6">
            <h2>Etapes</h2>
        </v-col>
        <v-col cols="12" sm="6" class="d-flex">
            <v-spacer></v-spacer>
            <v-btn prepend-icon="mdi-plus" variant="outlined" rounded color="green" @click="addStep">Ajouter une
                étape</v-btn>
        </v-col>
    </v-row>
    <create-step v-for="step in steps" :key="step.id" :step-number="step.stepNumber" :id="step.id" class="mb-2"
        @delete="handleDeleteStep"></create-step>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';
import CreateStep from './ui/CreateStep.vue';

const emit = defineEmits(['snackbar']);
let rules = ref([]);

let steps = ref([
    { id: self.crypto.randomUUID(), stepNumber: 1 }
]);

const addStep = () => {
    steps.value.push({ id: self.crypto.randomUUID(), stepNumber: steps.value.length + 1 });
}

function handleDeleteStep(id) {
    if (steps.value.length == 1) {
        emit('snackbar', { message: 'Au moins une étape est nécessaire', color: 'red' });
        return
    };
    steps.value = steps.value.filter(step => step.id != id);
    steps.value.forEach((step, index) => {
        step.stepNumber = index + 1;
    });
}
</script>

<style scoped></style>
