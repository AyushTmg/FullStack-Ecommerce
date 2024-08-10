import { jwtDecode } from "jwt-decode"
import api from "../../../api/api"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../../constant"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

export default function ProtectedRoute({ children }) {
    const [isAuthenticated, setAuthenticationStatus] = useState(null);
    const navigate = useNavigate();

    // ! Calling UseEffect Hook Which calls the authenticateUser function
    useEffect(() => {
        authenticateUser().catch(() => setAuthenticationStatus(false))
    })

    // ! For Refreshing Access Token
    async function refreshToken() {
        const refresh = localStorage.getItem(REFRESH_TOKEN)
        try {
            const res = await api.post("/auth/token/refresh/", {
                refresh: refreshToken,
            });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                setAuthenticationStatus(true)
            } else {
                setAuthenticationStatus(false)
            }
        } catch (error) {
            console.log(error);
            setAuthenticationStatus(false);
        }
    }

    async function authenticateUser() {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setAuthenticationStatus(false);
            return;
        }
        //! Now Decoding the token for checking its expiration
        const decoded = jwtDecode(token);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        if (tokenExpiration < now) {
            // ! If expired refreshing the access token by calling this function
            await refreshToken();
        } else {
            setAuthenticationStatus(true);
        }
    }

    if (isAuthenticated === null) {
        return <div>Loading...</div>;
    }

    // Routes to /login if the user is not logged in 
    return isAuthenticated ? children : navigate('/login')


}