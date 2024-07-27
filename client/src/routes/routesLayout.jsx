import { Routes, Route } from "react-router-dom";
import Home from "../pages/home/home";
import UserLogin from "../pages/login/login";
import UserRegister from "../pages/register/register";
import ProtectedRoute from "../component/common/protectedRoute/ProtectedRoute";
import PublicRoute from "../component/common/publicRoute/PublicRoute";


export default function RouteLayout() {
    return (
        <Routes>
            <Route path="/" element={
                <ProtectedRoute>
                    <Home />
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

            <Route path="*" element={<div>Page NotFound</div>} />
        </Routes>
    )
}
