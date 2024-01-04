<template>
    <v-card class="pa-5">
        <v-row align="center">
            <v-spacer></v-spacer>
            <v-col cols="12" sm="1">
                <v-btn icon="mdi-delete" @click="onDeleteButtonClicked"></v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" sm="3">
                <image-upload-with-preview width="150" height="150"></image-upload-with-preview>
            </v-col>
            <v-col cols="12" sm="9">
                <v-textarea variant="outlined" auto-grow v-model="content"></v-textarea>
            </v-col>

        </v-row>
    </v-card>
</template>

<script setup>
import { ref } from 'vue';
import ImageUploadWithPreview from './ImageUploadWithPreview.vue';

const props = defineProps({
    id: {
        type: [String],
        required: true
    },
    stepNumber: {
        type: [Number, String],
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