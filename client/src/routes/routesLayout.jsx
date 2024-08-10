import { Routes, Route } from "react-router-dom";
import Home from "../pages/home/home";
import UserLogin from "../pages/login/login";
import UserRegister from "../pages/register/register";
import ProtectedRoute from "../component/common/protectedRoute/ProtectedRoute";
import PublicRoute from "../component/common/publicRoute/PublicRoute";
import ForgotPassword from "../pages/forgotPassword/forgotPassword";
import ResetPassword from "../pages/resetPassword/resetPassword";
import ChangePassword from "../pages/changePassword/changePassword"

export default function RouteLayout() {
    return (
        <Routes>
            <Route path="/" element={
                <ProtectedRoute>
                    <Home />
                </ProtectedRoute>
            } />
            <Route path="/change-password" element={
                <ProtectedRoute>
                    <ChangePassword />
                </ProtectedRoute>
            } />
            <Route path="/login" element={
                <PublicRoute>
                    <UserLogin />
                </PublicRoute>
            } />
            <Route path="/register" element={
                <PublicRoute>
                    <UserRegister />
                </PublicRoute>
            } />
            <Route path="/forgot-password" element={
                <PublicRoute>
                    <ForgotPassword />
                </PublicRoute>
            } />
            <Route path="/reset-password/:uid/:token" element={
                <PublicRoute>
                    <ResetPassword />
                </PublicRoute>
            } />



            <Route path="*" element={<div>Page NotFound</div>} />
        </Routes>
    )
}
