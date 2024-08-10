import { useState } from "react"
import "./changePassword.css"
import { userChangePassword } from "../../services/auth/auth";
import { isAxiosError } from "axios";
import ToastMessage from "../../utils/toaster/toaster";
import { useNavigate } from 'react-router-dom';



export default function ChangePassword() {
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [newPasswordConfirmation, setNewPasswordConfirmation] = useState("");
    const [errors, setErrors] = useState({});
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors({});
        try {
            const response = await userChangePassword({
                old_password: oldPassword,
                new_password: newPassword,
                new_password_confirmation: newPasswordConfirmation
            })
            if (response.success) {
                // localStorage.clear()
                ToastMessage.success(response.message);
                navigate('/login')
            }
        } catch (error) {
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
            <div>Change Password</div>
            <form onSubmit={handleSubmit}>
                <div>
                    <input type="password" name="oldPassword" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} required />
                    {errors.old_password && <div className="text-danger">{errors.old_password}</div>}
                </div>

                <div>
                    <input type="password" name="newPassword" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
                    {errors.new_password && <div className="text-danger">{errors.new_password}</div>}
                </div>

                <div>
                    <input type="password" name="newPasswordConfirmation" value={newPasswordConfirmation} onChange={(e) => setNewPasswordConfirmation(e.target.value)} required />
                    {errors.new_password_confirmation && <div className="text-danger">{errors.new_password_confirmation}</div>}
                </div>

                <button type="submit" className="btn btn-primary ">Change Password</button>
            </form>
        </>
    )
}