import React, { useState } from "react";
import { Form, Input, Button, Card, Typography, message } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { logIn, storeUserId } from "../../services/auth";
import { storeAccessToken, storeUsername } from "../../services/auth";

const { Title, Text } = Typography;

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      const response = await logIn(values);
      storeAccessToken(response.data.access_token);
      storeUsername(response.data.username);
      storeUserId(response.data.user_id);
      message.success("Login successful!");
      navigate("/");
    } catch (error: any) {
      message.error(
        error?.response?.data?.detail || "Login failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-page__container">
        <Card className="login-page__card">
          <div className="login-page__header">
            <Title level={2} className="login-page__title">
              Welcome Back
            </Title>
            <Text className="login-page__subtitle">
              Please enter your details to sign in
            </Text>
          </div>

          <Form
            name="login_form"
            layout="vertical"
            onFinish={onFinish}
            autoComplete="on"
            className="login-page__form"
          >
            <Form.Item
              name="email"
              label="Email"
              rules={[{ required: true, message: "Please input your email!" }]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="Email"
                autoComplete="email"
                className="login-page__input"
              />
            </Form.Item>

            <Form.Item
              name="password"
              label="Password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="Password"
                autoComplete="current-password"
                className="login-page__input"
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                block
                className="login-page__button"
              >
                Sign In
              </Button>
            </Form.Item>
          </Form>

          <div className="login-page__footer">
            <Text type="secondary">
              Don't have an account? <a href="/sign-up">Sign up</a>
            </Text>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Login;
