import React, { useMemo, useState, useEffect } from "react";
import { Layout, Menu, Dropdown, Avatar, Space, Button, Image } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import {
  PictureOutlined,
  GlobalOutlined,
  LockOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
} from "@ant-design/icons";
import useIsMobile from "../../utils/isMobile";
import IMAGES from "../../assets/images";

export interface MenuItem {
  key: string;
  icon: React.ReactNode;
  onClick: () => void;
  children?: MenuItem[];
  disabled?: boolean;
  visible?: boolean;
}

const { Header, Content, Sider, Footer } = Layout;

const LayoutSection: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const navigate = useNavigate();
  const location = useLocation();
  const isMobile = useIsMobile();

  const [collapsed, setCollapsed] = useState<boolean>(false);
  const [selectedKey, setSelectedKey] = useState<string>("image-generation");

  useEffect(() => {
    if (isMobile) {
      setCollapsed(true);
    } else {
      setCollapsed(false);
    }
  }, [isMobile]);

  const menuItems: MenuItem[] = useMemo(
    () => [
      {
        key: "image-generation",
        icon: <PictureOutlined />,
        onClick: () => navigate("/"),
        visible: true,
      },
      {
        key: "public-library",
        icon: <GlobalOutlined />,
        onClick: () => navigate("/public-library"),
        visible: true,
      },
      {
        key: "private-library",
        icon: <LockOutlined />,
        onClick: () => navigate("/private-library"),
        visible: true,
      },
    ],
    [navigate]
  );

  const userMenuItems = [
    {
      key: "profile",
      label: "Profile",
      icon: <UserOutlined />,
      onClick: () => navigate("/profile"),
    },
    {
      key: "logout",
      label: "Logout",
      icon: <LogoutOutlined />,
      danger: true,
      onClick: () => handleLogout(),
    },
  ];

  const handleLogout = () => {
    // Implement logout logic here
    navigate("/login");
  };

  useEffect(() => {
    const pathSegments = location.pathname.split("/").filter(Boolean);
    const currentKey =
      pathSegments.length === 0 ? "image-generation" : pathSegments[0];
    setSelectedKey(currentKey);
  }, [location.pathname]);

  const formatLabel = (key: string) =>
    key.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <Layout className="layout__section">
      <Header className="layout__section__header">
        <div className="layout__section__header__left">
          <Button
            type="text"
            className="layout__section__toggle"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
          />

          <Image
            src={IMAGES.logo}
            preview={false}
            className="layout__section__logo"
          />
        </div>

        <div className="layout__section__header__right">
          <Dropdown menu={{ items: userMenuItems }} trigger={["click"]}>
            <div className="layout__section__user__dropdown">
              <Space>
                <Avatar icon={<UserOutlined />} />
                {isMobile ? null : <span className="user-name">John Doe</span>}
              </Space>
            </div>
          </Dropdown>
        </div>
      </Header>

      <Layout className="layout__section__body">
        <Sider
          trigger={null}
          collapsible
          collapsed={collapsed}
          width={220}
          collapsedWidth={isMobile ? 0 : 70}
          className={`layout__section__sider ${
            collapsed ? "collapsed" : "expanded"
          }`}
        >
          <Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            className="layout__section__menu"
            items={menuItems
              .filter((item) => item.visible !== false)
              .map((item) => ({
                key: item.key,
                icon: item.icon,
                onClick: () => {
                  item.onClick();
                  if (isMobile) setCollapsed(true);
                },
                label: formatLabel(item.key),
              }))}
          />
        </Sider>

        <Layout
          className={`layout__section__main ${collapsed ? "collapsed" : ""} ${
            isMobile ? "is-mobile" : ""
          }`}
        >
          <div className="layout__section__title">
            {formatLabel(selectedKey)}
          </div>
          <Content className="layout__section__content">{children}</Content>
          <Footer className="layout__section__footer">
            <div className="layout__section__footer__text">
              ©2025 Your Product Name
            </div>
          </Footer>
        </Layout>

        {/* Mask rendered only on mobile when menu is expanded */}
        {isMobile && !collapsed && (
          <div
            className="layout__section__mask"
            onClick={() => setCollapsed(true)}
          />
        )}
      </Layout>
    </Layout>
  );
};

export default LayoutSection;
