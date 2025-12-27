import axios, {
  /*AxiosRequestHeaders*/ AxiosResponse /*AxiosError*/,
} from "axios";

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// http.interceptors.request.use(
//   async (config) => {
//     const accessToken = retrieveAccessToken();
//     if (accessToken) {
//       config.headers = {
//         ...config.headers,
//         Authorization: `Bearer ${accessToken}`,
//       } as AxiosRequestHeaders;
//     }

//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// http.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   async (error) => {
//     const originalRequest = error.config;

//     if (error.response?.status === 401 && !originalRequest._retry) {
//       originalRequest._retry = true;

//       const refreshToken = retrieveRefreshToken();
//       if (refreshToken) {
//         try {
//           const response = await axios.post(ENDPOINT.refreshToken, {
//             refresh_token: refreshToken,
//           });

//           storeAccessToken(response?.data?.access_token);
//           storeRefreshToken(response?.data?.refresh_token);

//           originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
//           return http(originalRequest);
//         } catch (refreshError) {
//           const axiosError = refreshError as AxiosError;
//           if (axiosError.response?.status === 401) {
//             logOut();
//             message.error("Session expired. Please log in again.");
//             return Promise.reject(axiosError);
//           }
//         }
//       } else {
//         logOut();
//       }
//     }

//     return Promise.reject(error);
//   }
// );

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
