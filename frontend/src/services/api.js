import axios from 'axios';

const baseURL = `${import.meta.env.VITE_API_BASE_URL}:${import.meta.env.VITE_API_PORT}`;
console.log(import.meta.env.VITE_API_BASE_URL)

const api = axios.create({ baseURL });

export default api;
