/**
 * Centralized endpoint store
 * Modify the baseURL or set it to an appropriate env variable
*/
class UrlsConfig {
    static baseURL = 'http://localhost:8000/'; 
    
    static endpoints = {
        LOGIN:"api/auth/login/",
        REGISTER: "api/auth/signup/",
        REFRESH_ACCESS_TOKEN: "api/auth/refresh-access-token",
        OTP: "api/auth/otp/",
        VERIFY_PASSWORD: "api/auth/verify-password"
    };
}

export default UrlsConfig;
