import axios, { AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { retrieveAccessToken, logOutSessionExpired } from "./auth";

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 120000,
});

http.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = retrieveAccessToken();

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

http.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    if (
      error.response &&
      (error.response.status === 401 || error.response.status === 403)
    ) {
      logOutSessionExpired();
    }
    return Promise.reject(error);
  }
);

export const httpSubmitForm = async ({
  endpoint,
  formData,
  method,
}: {
  formData: FormData;
  endpoint: string;
  method: "post" | "put" | "patch";
}): Promise<AxiosResponse> =>
  await http({
    method: method,
    url: endpoint,
    headers: {
      "Content-Type": "multipart/form-data",
    },
    data: formData,
  });

export default http;
