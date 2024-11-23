import axios from "axios"

const url = "http://localhost:8000"

export const api = axios.create({
    baseURL: url,
})