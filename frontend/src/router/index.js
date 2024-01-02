import { createRouter, createWebHistory } from 'vue-router'
import RecipesList from '../pages/RecipesList.vue'
import RecipeView from '../pages/RecipeView.vue'
import RecipeAdd from '../pages/RecipeAdd.vue'
import FoodsList from '../pages/FoodsList.vue'
import TrackingJournal from '../pages/TrackingJournal.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: RecipesList
    },
    {
      path: '/foods',
      name: 'foods',
      component: FoodsList
    },
    {
      path: '/recipes',
      name: 'recipes',
      component: RecipesList
    },
    {
      path: '/recipes/:id',
      name: 'recipe_view',
      component: RecipeView
    },
    {
      path: '/recipes/add',
      name: 'recipe_add',
      component: RecipeAdd
    },
    {
      path: '/tracking',
      name: 'tracking',
      component: TrackingJournal
    },
  ]
})

export default router
