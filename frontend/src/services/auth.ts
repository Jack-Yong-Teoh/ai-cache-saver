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
    removeUsername();
    removeUserId();
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
  removeUsername();
  removeUserId();
  window.location.href = "/login";
};

export const storeUsername = (username: string) => {
  try {
    localStorage.setItem("USERNAME", username);
  } catch {
    message.error("Error storing username");
  }
};

export const retrieveUsername = () => {
  try {
    return localStorage.getItem("USERNAME");
  } catch {
    message.error("Error retrieving username");
    return null;
  }
};

export const removeUsername = () => {
  try {
    localStorage.removeItem("USERNAME");
  } catch {
    message.error("Error removing username");
  }
};

export const storeUserId = (userId: number) => {
  try {
    localStorage.setItem("USER_ID", userId.toString());
  } catch {
    message.error("Error storing user ID");
  }
};

export const retrieveUserId = () => {
  try {
    const userId = localStorage.getItem("USER_ID");
    return userId ? parseInt(userId, 10) : null;
  } catch {
    message.error("Error retrieving user ID");
    return null;
  }
};

export const removeUserId = () => {
  try {
    localStorage.removeItem("USER_ID");
  } catch {
    message.error("Error removing user ID");
  }
};
