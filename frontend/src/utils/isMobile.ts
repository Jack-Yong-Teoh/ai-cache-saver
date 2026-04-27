import { useEffect, useState } from "react";

const useIsMobile = () => {
  const getIsMobile = () =>
    typeof window !== "undefined" && window.innerWidth <= 430;

  const [isMobile, setIsMobile] = useState<boolean>(getIsMobile);

  useEffect(() => {
    const checkScreenSize = () => {
      setIsMobile(getIsMobile());
    };

    window.addEventListener("resize", checkScreenSize);
    return () => {
      window.removeEventListener("resize", checkScreenSize);
    };
  }, []);

  return isMobile;
};

export default useIsMobile;
