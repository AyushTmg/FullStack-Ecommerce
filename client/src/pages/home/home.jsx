import "./home.css"
import ToastMessage from "../../utils/toaster/toaster"
import { useNavigate } from "react-router-dom"

export default function Home() {
    const navigate = useNavigate()


    const handleLogout = () => {
        localStorage.clear()
        ToastMessage.success("Successfully Logged Out")
        return navigate('/login')
    }

    return (
        <>
            <div>HomePage</div>
            <button onClick={handleLogout}>Logout</button>
            <button onClick={() => { navigate('/change-password') }}>Change Password</button>

        </>
    )
}