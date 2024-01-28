import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import RecipesList from '../pages/RecipesList.vue'
import RecipeView from '../pages/RecipeView.vue'
import RecipeAdd from '../pages/RecipeAdd.vue'
import FoodsList from '../pages/FoodsList.vue'
import FoodView from '../pages/FoodView.vue'
import FoodAdd from '../pages/FoodAdd.vue'
import TrackingJournal from '../pages/TrackingJournal.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: RecipesList },
    { path: '/login', name: 'login', component: Login },
    { path: '/register', name: 'register', component: Register },
    { path: '/foods', name: 'foods', component: FoodsList },
    { path: '/foods/:id', name: 'food_view', component: FoodView },
    { path: '/foods/add', name: 'food_add', component: FoodAdd },
    { path: '/recipes', name: 'recipes', component: RecipesList },
    { path: '/recipes/:recipe_id', name: 'recipe_view', component: RecipeView },
    { path: '/recipes/add', name: 'recipe_add', component: RecipeAdd },
    { path: '/tracking', name: 'tracking', component: TrackingJournal },
  ]
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register']; // Les routes qui ne nécessitent pas d'authentification
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('access_token'); // Ou utilisez votre logique de store pour vérifier si l'utilisateur est connecté

  // Rediriger vers la page de login si l'authentification est nécessaire et l'utilisateur n'est pas connecté
  if (authRequired && !loggedIn) {
      return next('/login');
  }

  next();
});

export default router
