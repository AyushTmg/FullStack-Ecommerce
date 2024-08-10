import { useState } from "react"
import "./forgotPassword.css"
import { isAxiosError } from "axios";
import { userForgotPassword } from "../../services/auth/auth";
import ToastMessage from "../../utils/toaster/toaster";


export default function ForgotPassword() {
    const [email, setEmail] = useState("")


    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await userForgotPassword({ email })
            if (response.success) {
                ToastMessage.success(response.message);
                setEmail("");
            }
        } catch (error) {
            if (isAxiosError(error)) {
                ToastMessage.error(error.response.data.message);
                console.log(error.response)
            } else {
                ToastMessage.error("An unexpected error occurred.", error);
            }
        }

    }


    return (
        <>
            <div>Forgot password</div>
            <form onSubmit={handleSubmit}>
                <input type="email" name="email" value={email} onChange={(e) => { setEmail(e.target.value) }} required />
                <button className="btn btn-primary">Send Email</button>
            </form>
        </>
    )
}