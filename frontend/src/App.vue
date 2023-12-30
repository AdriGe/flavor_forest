<template>
  <v-card>
    <v-layout>
      <the-menu></the-menu>

      <v-main style="height: 100%">Hello</v-main>
    </v-layout>
  </v-card>
</template>

<script>
import TheMenu from './components/TheMenu.vue';

export default {
  components: {
    TheMenu
  }
}
</script>

<style scoped>

</style>
