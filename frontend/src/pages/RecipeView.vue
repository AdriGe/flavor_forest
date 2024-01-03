<template>

<recipe-filters></recipe-filters>
    <div>
        <v-card class="mx-auto my-8" max-width="60vw" elevation="16">
            <v-img gradient="to bottom, rgba(0,0,0,0), rgba(0,0,0,0), rgba(0,0,0,.33), rgba(0,0,0,.7)"
                class="align-end text-white" src="/src/assets/images/recipes/1.png" cover height="45vh">
                <v-card-item>
                    <v-card-title id="recipeTitle">
                        Conchiglie al pesto rosso
                    </v-card-title>
                    <v-card-subtitle id="recipeSubtitle">
                        saupoudrées de fromage & persil
                    </v-card-subtitle>
                </v-card-item>
            </v-img>
            <v-card-item>
                <v-row no-gutters class="ma-2">
                    <v-col cols="12" sm="3">
                        <span class="basic-info-header">Temps total</span>
                        <span class="basic-info-value">20 minutes</span>
                    </v-col>
                    <v-col cols="12" sm="3">
                        <span class="basic-info-header">Calories</span>
                        <span class="basic-info-value">797 kcal</span>
                    </v-col>
                    <v-col cols="12" sm="3">
                        <span class="basic-info-header">Difficulté</span>
                        <span class="basic-info-value">Facile</span>
                    </v-col>
                </v-row>
            </v-card-item>
            <v-divider></v-divider>



            <v-card-item>
                <v-chip color="green" class="mr-2 mt-2">Moins de CO2</v-chip>
                <v-chip color="orange" class="mr-2 mt-2">Peu de vaisselle</v-chip>
                <v-chip color="red" class="mr-2 mt-2">Epicé</v-chip>
                <v-chip color="green" class="mr-2 mt-2">Végétarien</v-chip>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Description</h2>
                <span>
                    Viva Italia ! Nous vous emmenons en Italie avec le goût intense du pesto
                    rouge de ce plat. Moins connu que le vert, il est tout aussi savoureux.
                    Composé de tomates séchées, il donne une délicieuse saveur méditerranéenne
                    à ces pâtes tandis que la salade apporte une note de fraîcheur !
                </span>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Ingrédients</h2>
                <v-row no-gutters class="ma-2">
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/1.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">1 pièce(s)</span>
                                <span class="food-name">Échalote</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/2.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">90 g</span>
                                <span class="food-name">Pesto rosso</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/3.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">50 g</span>
                                <span class="food-name">Tomates semi-séchées</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/4.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">1 sachet</span>
                                <span class="food-name">Salade</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/5.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">180 g</span>
                                <span class="food-name">Conchiglie</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/6.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">75 g</span>
                                <span class="food-name">Fromage frais aux herbes</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/7.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">½ sachet</span>
                                <span class="food-name">Persil</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/8.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">20 g</span>
                                <span class="food-name">Fromage râpé à l'italienne</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/9.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">2 cs</span>
                                <span class="food-name">Huile d'olive</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/10.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">selon le goût</span>
                                <span class="food-name">Sel & Poivre</span>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="6" class="mb-4">
                        <v-row>
                            <v-col cols="12" sm="2">
                                <v-img src="/src/assets/images/foods/11.avif" height="50px" class="ml-auto"></v-img>
                            </v-col>
                            <v-col sm="10">
                                <span class="food-quantity">1 cs</span>
                                <span class="food-name">Vinaigre balsamique noir</span>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <span></span>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item class="pa-5">
                <h2>Ustensiles</h2>
                <span>
                    <ul class="horizontal-list">
                        <li>Passoire</li>
                        <li>Casserole</li>
                        <li>Wok ou sauteuse</li>
                        <li>Saladier</li>
                    </ul>
                </span>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Instructions</h2>
                <v-row no-gutters class="mb-3">
                    <v-col cols="12" sm="4">
                        <v-img src="/src/assets/images/recipes/steps/1.avif">
                            <div class="step-number-box">
                                <div class="step-number">1</div>
                            </div>
                        </v-img>
                    </v-col>
                    <v-col cols="12" sm="8" class="pl-10 align-self-center">
                        <ul>
                            <li>Veillez à bien respecter les quantités indiquées à gauche pour préparer votre recette !</li>
                            <li>Portez une grande casserole d'eau salée à ébullition pour les pâtes.</li>
                            <li>Émincez l’échalote. Coupez les tomates séchées en petits dés.</li>
                            <li>Faites cuire les conchiglie 12-14 min dans la casserole d'eau salée. Égouttez-les et
                                réservez-les.</li>
                        </ul>
                    </v-col>
                </v-row>
                <v-row no-gutters class="mb-3">
                    <v-col cols="12" sm="4">
                        <v-img src="/src/assets/images/recipes/steps/2.avif">
                            <div class="step-number-box">
                                <div class="step-number">2</div>
                            </div>
                        </v-img>
                    </v-col>
                    <v-col cols="12" sm="8" class="pl-10 align-self-center">
                        <ul>
                            <li>Pendant ce temps, faites chauffer un filet d’huile d’olive dans un wok ou une sauteuse et
                                faites-y revenir l’échalote 2 min à feu moyen-doux.</li>
                            <li>Ajoutez les tomates séchées et poursuivez la cuisson 2-3 min en remuant. Salez et poivrez.
                            </li>
                            <li>Effeuillez et ciselez le persil.</li>
                        </ul>
                    </v-col>
                </v-row>
                <v-row no-gutters class="mb-3">
                    <v-col cols="12" sm="4">
                        <v-img src="/src/assets/images/recipes/steps/3.avif">
                            <div class="step-number-box">
                                <div class="step-number">3</div>
                            </div>
                        </v-img>
                    </v-col>
                    <v-col cols="12" sm="8" class="pl-10 align-self-center">
                        <ul>
                            <li>Ajoutez les conchiglie, le pesto rosso, et la moitié du fromage frais aux herbes au wok.
                                Faites réchauffer le tout 1 min.</li>
                            <li>Dans un saladier, faites une vinaigrette en mélangeant le vinaigre balsamique avec un filet
                                d’huile d’olive. Salez et poivrez.</li>
                            <li>Ajoutez la salade et mélangez bien.</li>

                        </ul>
                    </v-col>
                </v-row>
                <v-row no-gutters class="mb-3">
                    <v-col cols="12" sm="4">
                        <v-img src="/src/assets/images/recipes/steps/4.avif">
                            <div class="step-number-box">
                                <div class="step-number">4</div>
                            </div>
                        </v-img>
                    </v-col>
                    <v-col cols="12" sm="8" class="pl-10 align-self-center">
                        <ul>
                            <li>Servez la salade et les conchiglie dans les assiettes.</li>
                            <li>Garnissez avec le reste de fromage frais aux herbes, de fromage râpé et de persil.</li>
                        </ul>
                    </v-col>
                </v-row>
            </v-card-item>
            <v-divider></v-divider>
            <v-card-item>
                <h2>Valeurs nutritionnelles</h2>
                <v-data-table :items="items" :headers="headers" density="compact" :hover="true" :items-per-page="99">
                    <template v-slot:header.nutrient="{ column }">
                        <span class="nutritional-facts-header">
                            {{ column.title }}
                        </span>
                    </template>
                    <template v-slot:header.perPortion="{ column }">
                        <span class="nutritional-facts-header">
                            {{ column.title }}
                        </span>
                    </template>
                    <template v-slot:header.per100g="{ column }">
                        <span class="nutritional-facts-header">
                            {{ column.title }}
                        </span>
                    </template>
                    <template v-slot:bottom></template>
                </v-data-table>
            </v-card-item>
        </v-card>
    </div>
</template>

<script setup>

import RecipeFilters from '../components/RecipeFilters.vue';

components: {
    RecipeFilters
}
const items = [
    { nutrient: "Énergie (kJ)", perPortion: "3335kJ", per100g: "1174kJ" },
    { nutrient: "Énergie (kcal)", perPortion: "797kcal", per100g: "281kcal" },
    { nutrient: "Matières grasses", perPortion: "42.1g", per100g: "14.82g" },
    { nutrient: "dont acides gras saturés", perPortion: "13.4g", per100g: "4.72g" },
    { nutrient: "Glucides", perPortion: "77.8g", per100g: "27.39g" },
    { nutrient: "dont sucres", perPortion: "10g", per100g: "3.52g" },
    { nutrient: "Protéines", perPortion: "20.3g", per100g: "7.15g" },
    { nutrient: "Sel", perPortion: "2.61g", per100g: "0.92g" }
]


const headers = [
    { title: 'Nutriments', value: 'nutrient' },
    { title: 'Par portion (284g)', value: 'perPortion' },
    { title: 'Pour 100g', value: 'per100g' }
]
</script>

<style scoped>
#recipeTitle {
    font-size: 2rem;
}

#recipeSubtitle {
    font-size: 1.1rem;
}

.basic-info-header {
    display: block;
    font-size: 1.1rem;
    font-weight: bold;
}

.food-quantity {
    font-weight: bold;
    display: block;
}

.food-name {
    font-style: italic;
}

.horizontal-list li {
    display: inline-block;
    margin-right: 3rem;
}

.step-number-box {
    background-color: rgba(100, 100, 100, 0.25);
    position: absolute;
    padding: 5px;
    border-bottom-right-radius: 5px;
}

.step-number {
    width: 25px;
    height: 25px;
    line-height: 25px;
    border-radius: 50%;
    border: solid 1px;
    text-align: center;
    display: block;
}

.nutritional-facts-header {
    font-weight: bold;
    font-size: 1rem;
}
</style>