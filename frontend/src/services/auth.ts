import { message } from "antd";
import { ENDPOINT } from "./api-endpoints";
import http from "./http";

export const ACCESS_TOKEN = "ACCESS_TOKEN";

export const signUp = async (params: {
  username: string;
  email: string;
  password: string;
}) => {
  const response = await http.post(ENDPOINT.signup, params);
  return response;
};

export const logIn = async (params: { email: string; password: string }) => {
  const response = await http.post(ENDPOINT.login, params);
  return response;
};

export const logOut = async () => {
  try {
    await http.post(ENDPOINT.logout);
  } catch (error) {
    console.error("Logout backend call failed", error);
  } finally {
    removeAccessToken();
    window.location.href = "/login";
  }
};

export const storeAccessToken = (token: string) => {
  try {
    localStorage.setItem(ACCESS_TOKEN, token);
  } catch {
    message.error("Error storing access token");
  }
};

export const retrieveAccessToken = () => {
  try {
    return localStorage.getItem(ACCESS_TOKEN);
  } catch {
    message.error("Error retrieving access token");
    return null;
  }
};

export const removeAccessToken = () => {
  try {
    localStorage.removeItem(ACCESS_TOKEN);
  } catch {
    message.error("Error removing access token");
  }
};

export const logOutSessionExpired = () => {
  removeAccessToken();
  window.location.href = "/login";
};
