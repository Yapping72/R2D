import axios from 'axios';
import JwtHandler from '../Jwt/JwtHandler';
import UrlsConfig from './UrlsConfig';
import { PageNavigationService } from '../Pages/PageNavigationService';

class CustomError extends Error {
    constructor(message, data) {
        super(message);
        this.data = data;
    }
}

/**
 * Axios client configured to trigger the django backend.
 * Contains a request and response interceptor to standardize how requests and responses are handled
 */
const AxiosClient = axios.create({
    baseURL: UrlsConfig.baseURL,
    timeout: 10000, // Request timeout in milliseconds
});

/**
 * Request interceptor that appends JWT token to request header
 * */
AxiosClient.interceptors.request.use(config => {
    const token = JwtHandler.getToken();  // Retrieve token from storage
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;  // Append JWT to the Authorization header
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// Response interceptor to handle standardized responses
AxiosClient.interceptors.response.use(
    (response) => {
        // Handle successful response
        const { data } = response;
        if (data.success) {
            return data; // Return the data if the response indicates success
        } 
        else {
            const message = data.data.error || 'An unexpected error occurred'; // Use the message from response or a default message
            return Promise.reject(new CustomError(message, data)); // Reject the promise with a new custom error
        }
    },
    (error) => {
        if (error.response && error.response.data) {
            // If there is an error response from the server
            const { data } = error.response;
            // Create a custom error with the message from the server or a default message
            const customError = new CustomError(data.data.error || 'An error occurred', data);
            return Promise.reject(customError); // Reject the promise with the custom error
        } else {
            // For network errors or unexpected errors without a response
            const networkError = new CustomError('Unexpected Error'); // Create a generic network error
            return Promise.reject(networkError); // Reject the promise with the network error
        }
    }
);

export default AxiosClient;