<template>
    <v-row class="my-3">
        <v-spacer></v-spacer>
        <v-col cols="12" sm="6" class="d-flex">
            <v-spacer></v-spacer>
            <v-btn prepend-icon="mdi-plus" variant="outlined" rounded color="green" @click="addIngredient">Ajouter un
                ingrédient</v-btn>
        </v-col>
    </v-row>
    <v-card class="pa-5">
        <recipe-ingredient-select v-for="ingredient in ingredients" :key="ingredient.id" :id="ingredient.id" class="mb-2"
            @delete="handleDeleteIngredient"></recipe-ingredient-select>
    </v-card>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';

import RecipeIngredientSelect from './ui/RecipeIngredientSelect.vue';

const emit = defineEmits(['snackbar']);

let rules = ref([]);

let ingredients = ref([
    { id: self.crypto.randomUUID(), name: '', quantity: '', unit: '', portion: '' }
]);

const addIngredient = () => {
    ingredients.value.push({ id: self.crypto.randomUUID(), name: '', quantity: '', unit: '', portion: '' });
    console.log(ingredients.value);
}

function handleDeleteIngredient(id) {
    console.log(id);
    if (ingredients.value.length == 1) {
        emit('snackbar', { message: 'Au moins un ingrédient est nécessaire', color: 'red' })
        return
    };
    ingredients.value = ingredients.value.filter(ingredient => ingredient.id != id);
}
</script>

<style scoped></style>
