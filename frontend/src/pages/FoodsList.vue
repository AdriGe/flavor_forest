<template>
    <food-filters></food-filters>

    <div id="content">
        <h1>Food List</h1>
        <v-row no-gutters>
            <v-col cols="12" sm="4" class="pa-2" v-for="food in foods" :key="food.id" :food="food">

            </v-col>
        </v-row>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import FoodFilters from '../components/foods/FoodFilters.vue';

const foods = ref([])
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
