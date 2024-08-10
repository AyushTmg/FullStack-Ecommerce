import "./login.css"
import { useState } from "react";
import { userLogin } from "../../services/auth/auth";
import { useNavigate } from "react-router-dom";
import { isAxiosError } from "axios";
import ToastMessage from "../../utils/toaster/toaster";


export default function UserLogin() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate()

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await userLogin({
                email: email,
                password: password
            })

            if (response.success) {
                ToastMessage.success(response.message);
                navigate('/');
            }
        } catch (error) {
            if (isAxiosError(error)) {
                ToastMessage.error(error.response.data.message);
            } else {
                ToastMessage.error("Some error occured during user login");
                console.log(error)
            }
        }
    }

    return (
        <>
            <form onSubmit={handleLogin}>
                <div>
                    <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div>
                    <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>

                <button className="btn btn-primary">Login</button>
            </form>
            <div onClick={() => navigate('/forgot-password')}>Forgot Password</div>
            <div onClick={() => navigate('/register')}>Register</div>
        </>
    )
}