import axios, { AxiosResponse } from "axios";

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 120000,
});

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
