import api from "../../api/api"

export async function userRegister(payload) {
    const res = await api.post('auth/register/', payload)
    return res.data;
}
