<template>
  <v-container>
    <v-row align="center">
      <v-col cols="12" sm="8">
        <v-text-field variant="underlined" label="Ustensiles" @keyup.enter="addChip" v-model="textInput" :error-messages="errorMessages"></v-text-field>
      </v-col>
      <v-col cols="12" sm="4" class="d-flex">
        <v-spacer></v-spacer>
        <v-btn prepend-icon="mdi-plus" variant="outlined" rounded color="green" @click="addChip">Ajouter un
          ustensile</v-btn>
      </v-col>
      </v-row>
      <v-row>
      <v-col cols="12" sm="12">
        <v-chip class="mr-2" v-for="(chip, index) in chips" :key="chip" variant="outlined" closable @click:close="deleteChip(chip)">
          {{ chip }}
        </v-chip>
      </v-col>
    </v-row>

    <v-row>
      <v-col >

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const textInput = ref('');
const chips = ref([]);
const errorMessages = ref([]);

const addChip = () => {
  errorMessages.value = [];

  if (textInput.value) {
    if (chips.value.includes(textInput.value)) {
      errorMessages.value.push("Cet ustensible existe déjà.");
    } else {
      chips.value.push(textInput.value);
      textInput.value = '';
    }
  } else {
    errorMessages.value.push("Ce champ ne peut pas être vide.");
  }
};

const deleteChip = (chipToDelete) => {
  chips.value = chips.value.filter(chip => chip !== chipToDelete);
};
</script>
