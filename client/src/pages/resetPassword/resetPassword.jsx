import "./resetPassword.css"
import { useParams, useNavigate } from 'react-router-dom';
import { useState } from "react";
import { isAxiosError } from "axios";
import ToastMessage from "../../utils/toaster/toaster";
import { userResetPassword } from "../../services/auth/auth";



export default function ResetPassword() {
    const [password, setPassword] = useState("")
    const [passwordConfirmation, setPasswordConfirmation] = useState("")
    const [errors, setErrors] = useState({})
    const { uid, token } = useParams()
    const navigate = useNavigate()


    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await userResetPassword(
                {
                    password: password,
                    password_confirmation: passwordConfirmation
                }, uid, token
            )

            if (response.success) {
                // localStorage.clear()
                ToastMessage.success(response.message)
                navigate('/login')
            }
        }
        catch (error) {
            if (isAxiosError(error)) {
                ToastMessage.error(error.response.data.message);
                setErrors(error.response.data.errors);
                console.log(error)
            } else {
                ToastMessage.error("An unexpected error occurred while resetting password");
                console.log(error);
            }
        }
    }
    return (
        <>
            <div>Reset Password</div>
            <form onSubmit={handleSubmit}>
                <div>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    {errors.password && <div className="text-danger">{errors.password}</div>}
                </div>

                <div>
                    <input type="password" value={passwordConfirmation} onChange={(e) => setPasswordConfirmation(e.target.value)} />
                    {errors.password_confirmation && <div className="text-danger">{errors.password_confirmation}</div>}
                </div>
                <button className="btn btn-primary">Reset Password</button>
            </form>
        </>
    )
}