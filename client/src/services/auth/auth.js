import api from "../../api/api"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constant";


export async function userRegister(payload) {
    const res = await api.post('auth/register/', payload)
    return res.data;
}

export async function userLogin(payload) {
    const res = await api.post('auth/login/', payload)
    const response = res.data;
    if (response.success) {
        // ! If Success Setting Access And Refresh Token At Local Storage 
        localStorage.setItem(ACCESS_TOKEN, response.data.access)
        localStorage.setItem(REFRESH_TOKEN, response.data.refresh)

        console.log(localStorage.getItem(ACCESS_TOKEN))
    }
    return res.data;
}

export async function userForgotPassword(payoad) {
    const res = await api.post('auth/forgot-password/', payoad)
    return res.data;
}

export async function userResetPassword(payload, uid, token) {
    const res = await api.post(`auth/reset-password/${uid}/${token}/`, payload);
    return res.data
}

export async function userChangePassword(payload) {
    const res = await api.post('auth/change-password/', payload);
    return res.data;
}
