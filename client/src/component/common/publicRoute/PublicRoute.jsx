import { ACCESS_TOKEN } from "../../../constant";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function PublicRoute({ children }) {
    const [isChecking, setChecking] = useState(true);
    const navigate = useNavigate()

    useEffect(() => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            return navigate('/');
        } else {
            setChecking(false);
        }
    }, [navigate])

    if (isChecking) {
        return <div>Loading...</div>;
    }

    return children;

}