import React, { useState } from "react";
import { Form, Input, Button, Card, Typography, message } from "antd";
import { UserOutlined, LockOutlined, MailOutlined } from "@ant-design/icons";

const { Title, Text } = Typography;

const SignUp: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 1500));
      console.log("SignUp values:", values);
      message.success("Account created successfully!");
    } catch (error) {
      message.error("Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-page__container">
        <Card className="signup-page__card">
          <div className="signup-page__header">
            <Title level={2} className="signup-page__title">
              Create Account
            </Title>
            <Text className="signup-page__subtitle">
              Join us to start generating art
            </Text>
          </div>

          <Form
            name="signup_form"
            layout="vertical"
            onFinish={onFinish}
            autoComplete="on"
            className="signup-page__form"
          >
            <Form.Item
              name="username"
              label="Username"
              rules={[
                { required: true, message: "Please input your username!" },
              ]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="Username"
                autoComplete="username"
                className="signup-page__input"
              />
            </Form.Item>

            <Form.Item
              name="email"
              label="Email"
              rules={[
                { required: true, message: "Please input your email!" },
                {
                  type: "email",
                  message: "Please enter a valid email address!",
                },
              ]}
            >
              <Input
                prefix={<MailOutlined />}
                placeholder="Email address"
                autoComplete="email"
                className="signup-page__input"
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
                autoComplete="new-password"
                className="signup-page__input"
              />
            </Form.Item>

            <Form.Item
              name="confirm"
              label="Confirm Password"
              dependencies={["password"]}
              rules={[
                { required: true, message: "Please confirm your password!" },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue("password") === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(
                      new Error("The two passwords do not match!")
                    );
                  },
                }),
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="Confirm Password"
                autoComplete="new-password"
                className="signup-page__input"
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                block
                className="signup-page__button"
              >
                Sign Up
              </Button>
            </Form.Item>
          </Form>

          <div className="signup-page__footer">
            <Text type="secondary">
              Already have an account? <a href="/login">Sign in</a>
            </Text>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default SignUp;
