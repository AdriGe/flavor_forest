<template>
    <v-row class="mb-3" algn="center">
        <v-col cols="12" sm="9">
            <v-text-field variant="underlined" v-model="title" :rules="rules" label="Titre de la recette"></v-text-field>
            <v-text-field variant="underlined" v-model="subtitle" :rules="rules" label="Sous titre"></v-text-field>
        </v-col>

        <v-col cols="12" sm="3" class="d-flex">
            <v-spacer></v-spacer>
            <div>
                <image-upload-with-preview width="150" height="150"></image-upload-with-preview>
            </div>
        </v-col>
    </v-row>
    <v-row>
        <v-col cols="12" sm="12">
            <v-textarea variant="outlined" label="Description"></v-textarea>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref, computed } from 'vue';

import ImageUploadWithPreview from '../common/ui/ImageUploadWithPreview.vue';


let title = ref('');
let subtitle = ref('');
let rules = ref([]);




</script>

<style scoped></style>
