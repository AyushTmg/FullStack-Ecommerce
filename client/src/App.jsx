import { BrowserRouter } from 'react-router-dom'
import RouteLayout from './routes/routesLayout'
import { ToastContainer } from "react-toastify"
import "react-toastify/dist/ReactToastify.css";


function App() {


  return (
    <>
      <BrowserRouter>
        <RouteLayout />
      </BrowserRouter>

      <ToastContainer />
    </>
  )
}

export default App
