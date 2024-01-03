<template>
        <v-img :src="imageUrl" width="150" height="150" class="mx-auto" cover value="rounded-xl">
            <div id="fileInput" v-if="!imageUrl">
                <v-file-input prepend-icon="mdi-camera-plus-outline" variant="underlined"
                    label="&nbsp;&nbsp;&nbsp;&nbsp;Image" v-model="file" class="mx-auto" accept="image/*" density="compact">
                </v-file-input>
            </div>
            <div id="clearButton" v-if="imageUrl">
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
#content {
    width: 200px;
}

#imagePlaceholder {
    border: 2px gray dashed;
    border-radius: 20px;
    text-align: center;
}

#clearButton {
    text-align: right;
    margin-top: -7%;
}

#fileInput {
    border: 1px dashed gray;
    border-radius: 20px;
    padding: 1vw;
    vertical-align: middle;
    width: 100%;
    height: 100%;
    padding-top: 25%;
}

</style>