<template>
    <v-img :src="imageUrl" width="150" height="150" class="mx-auto" cover>
        <div id="fileInput" v-if="!imageUrl">
            <div id="inspire">
                <v-file-input prepend-icon="mdi-camera-plus-outline" v-model="file" accept="image/*">
                </v-file-input>
            </div>
        </div>
        <div id="clearButton" v-else>
            <v-btn class="mt-5" icon="mdi-close-circle" variant="text" @click="clearImage"></v-btn>
        </div>
    </v-img>
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

const clearImage = () => {
    file.value = null;
    imageUrl.value = null;
};

</script>

<style scoped>
#inspire :deep() .v-input__control {
    display: none;
}

#fileInput {
    border: 1px dashed gray;
    border-radius: 20px;
    width: 100%;
    height: 100%;
}

#inspire {
    position: absolute;
    top: 59px;
    left: 59px;
}

#clearButton {
    position: absolute;
    top: -1em;
    right: 0;
}


</style>