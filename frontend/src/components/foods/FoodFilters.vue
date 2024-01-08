<template>
    <v-app-bar>
        <v-row align="center" no-gutters>
            <v-spacer></v-spacer>
            <v-col cols="10" sm="6">
                <v-text-field rounded density="compact" variant="outlined" v-model="searchText"
                    label="Rechercher un aliment" hide-details="true">
                </v-text-field>
            </v-col>
            <v-col cols="10" sm="2" class="d-flex">
                <v-spacer />
                <router-link to="/foods/add">
                    <v-btn prepend-icon="mdi-plus" variant="outlined" rounded color="green">Ajouter</v-btn>
                </router-link>
            </v-col>
            <v-spacer></v-spacer>
        </v-row>
    </v-app-bar>
</template>

<script setup>
import { ref } from 'vue';

let searchText = ref('');


</script>
