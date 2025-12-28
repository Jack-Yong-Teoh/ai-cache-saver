import { ENDPOINT } from "./api-endpoints";
import http from "./http";
import { sprintf } from "sprintf-js";

export interface GenerateImageParams {
  prompt_text: string;
  user_id: number;
  is_public?: boolean;
}

export const generateImage = async (params: GenerateImageParams) => {
  const response = await http.post(ENDPOINT.generateImage, null, {
    params: {
      prompt_text: params.prompt_text,
      user_id: params.user_id,
      is_public: params.is_public ?? true,
    },
  });
  return response?.data;
};

export const getPromptImages = async (params: any) => {
  const response = await http.post(sprintf(ENDPOINT.getPromptImages), params);
  return response.data;
};
