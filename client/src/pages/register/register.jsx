import "./register.css"
import { userRegister } from "../../services/auth/auth"
import { useState } from "react"
import { isAxiosError } from "axios";
import { useNavigate } from "react-router-dom"
import ToastMessage from "../../utils/toaster/toaster";


export default function UserRegister() {
    const [firstname, setFirstName] = useState("")
    const [lastname, setLastName] = useState("")
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [passwordConfirmation, setPasswordConfirmation] = useState("")
    const [errors, setErrors] = useState({})

    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await userRegister({
                first_name: firstname,
                last_name: lastname,
                username: username,
                email: email,
                password: password,
                password_confirmation: passwordConfirmation
            })
            if (response.success) {
                ToastMessage.success(response.message);
                return navigate('/login');
            }
        } catch (error) {
            if (isAxiosError(error)) {
                setErrors(error.response.data.errors)
                ToastMessage.error(error.response.data.message);
            } else {
                console.log(error)
                ToastMessage.error("Some error occured during user registration");
            }
        }
    }



    return (
        <>
            <form onSubmit={handleSubmit}>

                <div>
                    <input type="text" name="firstname" placeholder="firstname" required value={firstname} onChange={(e) => { setFirstName(e.target.value) }} />
                    {errors.first_name && <div className="text-danger">{errors.first_name}</div>}
                </div>
                <div>
                    <input type="text" name="lastname" placeholder="lastname" required value={lastname} onChange={(e) => { setLastName(e.target.value) }} />
                    {errors.last_name && <div className="text-danger">{errors.last_name}</div>}
                </div>
                <div>
                    <input type="text" name="username" placeholder="username" required value={username} onChange={(e) => { setUsername(e.target.value) }} />
                    {errors.username && <div className="text-danger">{errors.username}</div>}

                </div>
                <div>
                    <input type="email" name="email" placeholder="email" required value={email} onChange={(e) => { setEmail(e.target.value) }} />
                    {errors.email && <div className="text-danger">{errors.email}</div>}

                </div>
                <div>
                    <input type="password" name="password" placeholder="password" required value={password} onChange={(e) => { setPassword(e.target.value) }} />
                    {errors.password && <div className="text-danger">{errors.password}</div>}

                </div>
                <div>
                    <input type="password" name="passwordConfirmation" placeholder="password Confiramtion" required value={passwordConfirmation} onChange={(e) => { setPasswordConfirmation(e.target.value) }} />
                    {errors.password_confirmation && <div className="text-danger">{errors.password_confirmation}</div>}

                </div>

                <button className="btn btn-primary" type="submit">Register</button>

            </form>

            <div onClick={() => navigate('/login')}>Login</div>

        </>
    )
}