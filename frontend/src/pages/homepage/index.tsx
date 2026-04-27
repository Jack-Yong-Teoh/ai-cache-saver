import React, { useState } from "react";
import { Form, Input, Button, Switch, Image, message } from "antd";
import { QuestionOutlined, LoadingOutlined } from "@ant-design/icons";
import { generateImage } from "../../services/imageGeneration";

interface GeneratedImage {
  url: string;
}

const USER_ID = 1;

const HomePage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);
  const [generatedImage, setGeneratedImage] = useState<GeneratedImage | null>(
    null
  );

  const onFinish = async (values: { prompt: string; isPublic: boolean }) => {
    setLoading(true);
    setGeneratedImage(null);

    try {
      const response = await generateImage({
        prompt_text: values.prompt,
        user_id: USER_ID,
        is_public: values.isPublic,
      });

      if (response && response.image_url) {
        setGeneratedImage({ url: response.image_url });
        form.resetFields(["prompt"]);
        message.success("Image generated successfully!");
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      message.error("Failed to generate image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="homepage">
      <div className="homepage__prompt-section">
        <div className="homepage__generation-area">
          <Form
            form={form}
            onFinish={onFinish}
            layout="vertical"
            initialValues={{ isPublic: true }}
            className="homepage__form"
          >
            <Form.Item
              name="prompt"
              label="Image Prompt"
              rules={[{ required: true, message: "Please enter a prompt!" }]}
              className="homepage__form-item"
            >
              <Input.TextArea
                autoSize={{ minRows: 3, maxRows: 3 }}
                placeholder="Describe the image you want to generate..."
                className="homepage__textarea"
              />
            </Form.Item>

            <Form.Item
              name="isPublic"
              label="Make Public"
              valuePropName="checked"
              tooltip="Public images appear in the gallery and act as generation references for others."
              className="homepage__form-item homepage__form-item--switch"
            >
              <Switch className="homepage__switch" />
            </Form.Item>

            <Form.Item className="homepage__form-item homepage__form-item--actions">
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                block
                className="homepage__generate-btn"
              >
                Generate Image
              </Button>
            </Form.Item>
          </Form>
        </div>
      </div>

      <div className="homepage__image-section">
        <div className="homepage__display-area">
          <div className="homepage__image-container">
            {loading ? (
              <div className="homepage__loader">
                <div className="homepage__loader__skeleton"></div>
                <div className="homepage__loader__content">
                  <LoadingOutlined className="homepage__loader__spinner" />
                  <p className="homepage__loader__text">
                    Generating your masterpiece...
                  </p>
                </div>
              </div>
            ) : generatedImage ? (
              <Image
                src={generatedImage.url}
                alt="Generated"
                className="homepage__generated-image"
              />
            ) : (
              <div className="homepage__empty-state">
                <QuestionOutlined className="homepage__empty-icon" />
                <p className="homepage__empty-text">No image generated yet</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
