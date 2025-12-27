import React, { useEffect } from "react";

const ScrollRestoration: React.FC = () => {
  const scrollKey = "scroll-position";

  const saveScrollPosition = () => {
    localStorage.setItem(scrollKey, window.scrollY.toString());
  };

  const restoreScrollPosition = () => {
    const savedPosition = localStorage.getItem(scrollKey);
    if (savedPosition) {
      window.scrollTo(0, parseFloat(savedPosition));
    }
  };

  useEffect(() => {
    restoreScrollPosition();
    window.addEventListener("scroll", saveScrollPosition);
    return () => {
      window.removeEventListener("scroll", saveScrollPosition);
    };
  }, []);

  return null;
};

export default ScrollRestoration;
