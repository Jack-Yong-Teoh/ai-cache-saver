import React, { useState, useEffect } from "react";
import {
  Form,
  Input,
  Button,
  Card,
  Image,
  Empty,
  Pagination,
  Spin,
  Modal,
  Typography,
  Descriptions,
  Tag,
  message,
} from "antd";
import {
  SearchOutlined,
  InfoCircleOutlined,
  CalendarOutlined,
} from "@ant-design/icons";
import { getPromptImages } from "../../services/imageGeneration";
import dayjs from "dayjs";

const { Title, Paragraph, Text } = Typography;

const PrivateLibrary: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);
  const [images, setImages] = useState<any[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);

  const [modalVisible, setModalVisible] = useState(false);
  const [selectedImage, setSelectedImage] = useState<any>(null);

  const PAGE_SIZE = 50;

  const fetchImages = async (page: number = 1) => {
    setLoading(true);
    const values = form.getFieldsValue();

    // Updated Filters: Private images for specific user
    const filters: any[] = [
      { field: "is_public", operator: "is", value: false },
      { field: "user_id", operator: "equals", value: 1 },
    ];

    if (values.prompt) {
      filters.push({
        field: "prompt_text",
        operator: "contains",
        value: values.prompt,
      });
    }

    const payload = {
      filters: filters,
      pagination: { limit: PAGE_SIZE, page: page },
      sort: { order_by: "id", sort_order: "desc" },
    };

    try {
      const res = await getPromptImages(payload);
      setImages(res?.data || []);
      setTotal(res?.count || 0);
      setCurrentPage(page);
    } catch (error: any) {
      message.error(error?.response?.data?.detail || "Failed to fetch images.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleImageClick = (img: any) => {
    setSelectedImage(img);
    setModalVisible(true);
  };

  const handleModalClose = () => {
    setModalVisible(false);
    setTimeout(() => setSelectedImage(null), 300);
  };

  const formatDate = (dateString: string) => {
    return dayjs(dateString).format("MMMM D, YYYY, h:mm A");
  };

  return (
    <div className="private-library">
      <div className="private-library__header">
        <div className="private-library__header-content">
          <Title level={2} className="private-library__title">
            My Private Gallery
          </Title>
          <Text className="private-library__subtitle">
            Manage and view your personal generated artwork.
          </Text>
        </div>

        <Card className="private-library__search-bar">
          <Form
            form={form}
            layout="inline"
            onFinish={() => fetchImages(1)}
            className="private-library__form"
          >
            <Form.Item
              name="prompt"
              className="private-library__form-item__input"
              style={{ flex: 1 }}
            >
              <Input
                prefix={<SearchOutlined className="text-gray-400" />}
                placeholder="Search your private prompts..."
                allowClear
                size="large"
              />
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                icon={<SearchOutlined />}
                size="large"
                className="private-library__search-btn"
              >
                Search
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </div>

      <div className="private-library__content">
        {loading ? (
          <div className="private-library__loader">
            <Spin size="large" />
            <div className="private-library__loader-text">
              Loading your gallery...
            </div>
          </div>
        ) : images.length > 0 ? (
          <>
            <div className="private-library__grid">
              {images.map((img) => (
                <Card
                  key={img.id}
                  className="private-library__image-card"
                  hoverable
                  onClick={() => handleImageClick(img)}
                  cover={
                    <div className="private-library__image-wrapper">
                      <Image
                        src={img.image_url}
                        alt={img.prompt_text}
                        preview={false}
                        fallback="https://placehold.co/400x400?text=Image+Not+Found"
                      />
                      <div className="private-library__card-hover-icon">
                        <InfoCircleOutlined />
                      </div>
                    </div>
                  }
                />
              ))}
            </div>

            <div className="private-library__pagination">
              <Pagination
                current={currentPage}
                total={total}
                pageSize={PAGE_SIZE}
                onChange={(page) => fetchImages(page)}
                showSizeChanger={false}
              />
            </div>
          </>
        ) : (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              <div className="flex flex-col items-center gap-2">
                <Text type="secondary">
                  You haven't generated any private images yet.
                </Text>
              </div>
            }
            className="private-library__empty"
          />
        )}
      </div>

      <Modal
        open={modalVisible}
        onCancel={handleModalClose}
        footer={null}
        centered
        width={1000}
        className="private-library__modal"
        destroyOnClose
      >
        {selectedImage && (
          <div className="private-library__modal-content">
            <div className="private-library__modal-image-container">
              <Image
                src={selectedImage.image_url}
                alt={selectedImage.prompt_text}
                preview={false}
                className="private-library__modal-image"
                placeholder={<Spin />}
              />
            </div>

            <div className="private-library__modal-details">
              <div className="private-library__modal-details-inner">
                <Descriptions
                  title="Image Details"
                  column={1}
                  layout="vertical"
                  size="small"
                >
                  <Descriptions.Item
                    label={
                      <span className="font-semibold text-slate-500">
                        Prompt
                      </span>
                    }
                  >
                    <Paragraph
                      className="mb-0 font-medium text-gray-700"
                      ellipsis={{
                        rows: 8,
                        expandable: true,
                        symbol: "show more",
                      }}
                    >
                      {selectedImage.prompt_text}
                    </Paragraph>
                  </Descriptions.Item>
                  <Descriptions.Item
                    label={
                      <span className="font-semibold text-slate-500">
                        <CalendarOutlined className="mr-1" /> Created Date
                      </span>
                    }
                  >
                    <Text className="text-gray-600">
                      {formatDate(selectedImage.created_date)}
                    </Text>
                  </Descriptions.Item>
                  <Descriptions.Item
                    label={
                      <span className="font-semibold text-slate-500">
                        Image ID
                      </span>
                    }
                  >
                    <Tag color="blue">{selectedImage.id}</Tag>
                    <Tag color="orange">Private</Tag>
                  </Descriptions.Item>
                </Descriptions>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default PrivateLibrary;
