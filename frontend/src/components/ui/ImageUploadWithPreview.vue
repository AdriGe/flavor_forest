<template>
    <v-img :src="imageUrl" :width="width" :height="height" class="mx-auto" cover>
        <div id="fileInput" v-if="!imageUrl">
            <div id="inspire" :style="inspireStyle">
                <v-file-input prepend-icon="mdi-camera-plus-outline" v-model="file" accept="image/*">
                </v-file-input>
            </div>
        </div>
        <div id="clearButton" v-else>
            <v-btn class="mt-5" icon="mdi-close-circle" density="compact" @click="clearImage"></v-btn>
        </div>
    </v-img>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  width: {
    type: [Number, String],
    default: 150
  },
  height: {
    type: [Number, String],
    default: 150
  }
});

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

const inspireStyle = computed(() => {
  const top = parseInt(props.height) / 2 - 16 + 'px';
  const left = parseInt(props.width) / 2 - 16 + 'px';
  return { top, left };
});

</script>

<style scoped>
#inspire :deep() .v-input__control {
    display: none;
}

#inspire {
    position: absolute;
}

#fileInput {
    border: 1px dashed gray;
    border-radius: 20px;
    width: 100%;
    height: 100%;
}


#clearButton {
    position: absolute;
    top: -1em;
    right: 0;
}


</style>