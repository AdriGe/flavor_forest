<template>
    <v-card class="px-5 pt-2 pb-2" width="300" height="300">
        <v-file-input prepend-icon="mdi-camera-plus-outline" variant="underlined" label="Image d'illustration"
            v-model="file" class="mx-auto" accept="image/*" density="compact">

            <template v-slot:selection="{ fileNames }">
                {{ truncateFileName(fileNames[0]) }}
            </template>
        </v-file-input>
        <v-img :src="imageUrl" width="300" height="200" class="mx-auto" cover>
            <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height" id="imagePlaceholder">
                    Aucune image sélectionnée
                </div>
            </template>
        </v-img>
    </v-card>
</template>

<script setup>
import { ref, watch } from 'vue';

let imageUrl = ref(null);
let file = ref(null);

watch(file, (newValue) => {
    if (newValue && newValue.length > 0) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imageUrl.value = e.target.result;
        };
        reader.readAsDataURL(newValue[0]);
    } else {
        imageUrl.value = null;
    }
});

const truncateFileName = (fileName) => {
    const maxLength = 15; // Define the maximum length of the file name
    if (fileName.length > maxLength) {
        return fileName.substring(0, maxLength) + '...'; // Truncate and add ellipsis
    }
    return fileName;
};
</script>

<style scoped>
#content {
    width: 200px;
}

#imagePlaceholder {
    border: 2px gray dashed;
    border-radius: 20px;
    text-align: center;
}
</style>