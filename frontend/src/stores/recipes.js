// stores/recipes.js
import { defineStore } from 'pinia';

export const useRecipesStore = defineStore('recipes', {
  state: () => ({
    recipes: {} // This will store recipes with their IDs as keys
  }),
  actions: {
    addRecipe(recipe) {
      // Add new recipe with a timestamp
      this.recipes[recipe.recipe_id] = { data: recipe, timestamp: Date.now() };

      // Remove the oldest recipe if the limit is exceeded
      if (Object.keys(this.recipes).length > this.maxRecipes) {
        const oldestId = Object.keys(this.recipes).sort((a, b) => 
          this.recipes[a].timestamp - this.recipes[b].timestamp
        )[0];
        delete this.recipes[oldestId];
      }
    },
    addRecipes(recipesArray) {
      for (const recipe of recipesArray) {
        this.addRecipe(recipe);
      }
    }
  }
});
