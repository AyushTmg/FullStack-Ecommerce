import { Routes, Route } from "react-router-dom";

export default function RouteLayout() {
    return (
        <Routes>
            <Route path="/dummy" element={<div>Ayush</div>} />
            <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
    )
}
