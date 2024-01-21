<template>
    <router-link :to="`/recipes/${recipe_id}`">
        <v-card class="mx-auto my-8" max-width="20vw" height="380px" elevation="16">
            <v-img class="align-end text-white" height="200" :src="'/src/assets/images/recipes/'+image_url" cover>
            </v-img>

            <v-card-item>
                <v-card-title class="text-subtitle-1">
                    {{ name }}
                </v-card-title>
                <v-card-subtitle class="text-body-2">
                    {{ headline }}
                </v-card-subtitle>
            </v-card-item>

            <v-card-text>
                <v-chip v-for="tag in tags" :key="tag.tag_id" :color="getTagColor(tag.name)" class="mr-2 mt-2">
                    {{ tag.name }}
                </v-chip>
            </v-card-text>
        </v-card>
    </router-link>
</template>

<script setup>

const props = defineProps({
    name: String,
    headline: String,
    image_url: String,
    tags: Array,
    recipe_id: String // Assuming you need an ID for the router link
});

const getTagColor = (tag) => {
    // Define logic to determine the color of the tag based on its value
    // Example:
    switch (tag) {
        // Dietary Regime
        case 'Végétarien': return '#004d00'; // Darker Green
        case 'Vegan': return '#2e8b57'; // Sea Green
        case 'Sans gluten': return '#996515'; // Dark Goldenrod
        case 'Cétogène': return '#00008b'; // Dark Blue
        case 'Paleo': return '#654321'; // Darker Brown
        case 'Faible en glucides': return '#daa520'; // Goldenrod
        case 'Faible en calories': return '#4682b4'; // Steel Blue
        case 'Riche en protéines': return '#8b0000'; // Dark Red
        case 'Riche en légumes': return '#228b22'; // Forest Green
        case 'Détox': return '#3cb371'; // Medium Sea Green
        case 'Pescétarien': return '#00008b'; // Dark Blue
        case 'Flexitarien': return '#ff4500'; // Orange Red

        // Meal Type
        case 'Entrée': return '#4b0082'; // Indigo
        case 'Plat Principal': return '#800000'; // Maroon
        case 'Dessert': return '#db7093'; // Pale Violet Red
        case 'Amuse-bouche': return '#e9967a'; // Dark Salmon
        case 'Accompagnement': return '#696969'; // Dim Gray
        case 'Soupe': return '#6a5acd'; // Slate Blue
        case 'Salade': return '#2e8b57'; // Sea Green
        case 'Apéritif': return '#8b0000'; // Dark Red
        case 'Snack': return '#b8860b'; // Dark Goldenrod
        case 'Boisson': return '#20b2aa'; // Light Sea Green

        // Culinary Style
        case 'Turc': return '#8b4513'; // Saddle Brown
        case 'Vietnamienne': return '#556b2f'; // Dark Olive Green
        case 'Français': return '#00008b'; // Dark Blue
        case 'Britannique': return '#8b0000'; // Dark Red
        case 'Japonais': return '#8b0000'; // Dark Red
        case 'Moyen-Orient': return '#8b4513'; // Saddle Brown
        case 'Libanaise': return '#556b2f'; // Dark Olive Green
        case 'Chinois': return '#8b0000'; // Dark Red
        case 'Mexicain': return '#8b0000'; // Dark Red
        case 'Indien': return '#b8860b'; // Dark Goldenrod
        case 'Européen': return '#00008b'; // Dark Blue
        case 'Asiatique': return '#8b008b'; // Dark Magenta
        case 'Africain': return '#daa520'; // Goldenrod
        case 'Internationale': return '#ff6347'; // Tomato
        case 'Italien': return '#006400'; // Dark Green
        case 'Grec': return '#00008b'; // Dark Blue
        case 'Espagnol': return '#8b0000'; // Dark Red
        case 'Méditerranéen': return '#00008b'; // Dark Blue
        case 'Scandinave': return '#1e90ff'; // Dodger Blue
        case 'Coréenne': return '#a52a2a'; // Brown
        case 'Marocain': return '#191970'; // Midnight Blue
        case 'Latino-Américaine': return '#228b22'; // Forest Green
        case 'Américain': return '#00008b'; // Dark Blue
        case 'Thaï': return '#ba55d3'; // Medium Orchid

        default: return '#404040'; // Darker Grey (default color)
    }
};
</script>

<style scoped>
a {
   text-decoration: none;
}
</style>
