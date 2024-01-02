<template>
  <v-card>
    <v-layout>
      <the-menu></the-menu>

      <v-main style="height: 100%">
        <router-view v-slot="slotProps">
          <component :is="slotProps.Component"></component>
        </router-view>
      </v-main>
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
