const BASE_URL = import.meta.env.VITE_API_BASE_URL; // get in the .env file

export const ENDPOINT = {
  generateImage: `${BASE_URL}/prompt-image/generate`,
  getPromptImages: `${BASE_URL}/prompt-images`,
  signup: `${BASE_URL}/auth/signup`,
  login: `${BASE_URL}/auth/login`,
  logout: `${BASE_URL}/auth/logout`,
};
