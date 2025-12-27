import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ROUTES } from "./Routes";
import { ScrollRestoration } from "../components";
import HonmePage from "../pages/homepage";
// import { PublicRoute } from "./PublicRouter";
// import { PrivateRoute } from "./PrivateRouter";

const Router = () => {
  return (
    <Routes>
      <Route path={ROUTES.default} element={<HonmePage />} />
    </Routes>
  );
};

export default function SiteRouter() {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true, //console log warnings
        v7_relativeSplatPath: true,
      }}
    >
      <ScrollRestoration />
      <Router />
    </BrowserRouter>
  );
}
