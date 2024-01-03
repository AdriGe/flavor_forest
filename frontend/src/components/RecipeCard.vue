<template>
    <router-link to="/recipes/1">
    <v-card class="mx-auto my-8" max-width="20vw" elevation="16">
        <v-img class="align-end text-white" height="200" src="/src/assets/images/recipes/1.png" cover>

        </v-img>

        <v-card-item>
            <v-card-title>
                Conchiglie al pesto rosso
            </v-card-title>
            <v-card-subtitle>
                saupoudrées de fromage & persil
            </v-card-subtitle>
        </v-card-item>

        <v-card-text>
            <v-chip color="green" class="mr-2 mt-2">Moins de CO2</v-chip>
            <v-chip color="orange" class="mr-2 mt-2">Peu de vaisselle</v-chip>
            <v-chip color="red" class="mr-2 mt-2">Epicé</v-chip>
            <v-chip color="green" class="mr-2 mt-2">Végétarien</v-chip>
        </v-card-text>
    </v-card>
</router-link>
</template>

<script>


export default {
    name: 'RecipeCard',

    setup() {

        return {

        };
    },
};
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>
