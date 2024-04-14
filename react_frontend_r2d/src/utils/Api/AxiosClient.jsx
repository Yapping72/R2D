import axios from 'axios';
import JwtHandler from '../Jwt/JwtHandler';

// Create an Axios instance
const AxiosClient = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 10000, // Request timeout in milliseconds
});

// Request interceptor
AxiosClient.interceptors.request.use(config => {
    const token = JwtHandler.getToken();  // Retrieve token from storage
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;  // Append JWT to the Authorization header
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export default AxiosClient;
