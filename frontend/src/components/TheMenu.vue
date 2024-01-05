<template>
<v-navigation-drawer
        expand-on-hover
        rail
      >
        <v-list>
          <v-list-item
            prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
            title="Sandra Adams"
            subtitle="sandra_a88@gmailcom"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
            <v-list-item to="/foods" link prepend-icon="mdi-carrot" title="Aliments" value="foods"></v-list-item>
            <v-list-item to="/recipes" link prepend-icon="mdi-chef-hat" title="Recettes" value="recipes"></v-list-item>
            <v-list-item to="/tracking" link prepend-icon="mdi-book-open-variant-outline" title="Suivi" value="tracking"></v-list-item>
            <v-list-item to="/login" link prepend-icon="mdi-login" title="Connexion" value="login"></v-list-item>
            <v-list-item to="/signup" link prepend-icon="mdi-account-plus-outline" title="Inscription" value="signup"></v-list-item>

        </v-list>
      </v-navigation-drawer>
</template>

<style scoped>

</style>
