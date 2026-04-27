import { Navigate, useLocation } from "react-router-dom";

import { retrieveAccessToken } from "../services/auth";

import { ROUTES } from "./Routes";

export const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  // const auth = true;
  const auth = retrieveAccessToken();
  const location = useLocation();
  return auth ? (
    children
  ) : (
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    <Navigate to={ROUTES.logIn} state={{ from: location }} replace />
  );
};
