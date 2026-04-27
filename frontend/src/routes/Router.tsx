import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ROUTES } from "./Routes";
import { ScrollRestoration } from "../components";
import HomePage from "../pages/homepage";
import PrivateLibrary from "../pages/privateLibrary";
import PublicLibrary from "../pages/publicLibrary";
import LayoutSection from "../components/LayoutSection/LayoutSection";
import Login from "../pages/login";
import SignUp from "../pages/signUp";

import { PrivateRoute } from "./PrivateRouter";

const Router = () => {
  return (
    <Routes>
      <Route
        path={ROUTES.default}
        element={
          <PrivateRoute>
            <LayoutSection>
              <HomePage />
            </LayoutSection>
          </PrivateRoute>
        }
      />
      <Route
        path={ROUTES.publicLibrary}
        element={
          <PrivateRoute>
            <LayoutSection>
              <PublicLibrary />
            </LayoutSection>
          </PrivateRoute>
        }
      />
      <Route
        path={ROUTES.privateLibrary}
        element={
          <PrivateRoute>
            <LayoutSection>
              <PrivateLibrary />
            </LayoutSection>{" "}
          </PrivateRoute>
        }
      />
      <Route path={ROUTES.logIn} element={<Login />} />
      <Route path={ROUTES.signUp} element={<SignUp />} />s
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
