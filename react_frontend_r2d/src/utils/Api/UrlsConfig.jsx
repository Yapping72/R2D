/**
 * Backend Django API endpoints
 * @param {string} BaseUrl - "http://localhost:8000/"
 * @param {string} LOGIN - "api/auth/login/",
 * @param {string} REGISTER - "api/auth/signup/",
 * @param {string} REFRESH_ACCESS_TOKEN - "api/auth/refresh-access-token",
 * @param {string} OTP - "api/auth/otp/",
 * @param {string} VERIFY_PASSWORD - "api/auth/verify-password"
 */
class UrlsConfig {
    static baseURL = 'http://localhost:8000/';
    
    /**
     * Backend Django API endpoints
     * @param {string} BaseUrl - "http://localhost:8000/"
     * @param {string} LOGIN - "api/auth/login/",
     * @param {string} REGISTER - "api/auth/signup/",
     * @param {string} REFRESH_ACCESS_TOKEN - "api/auth/refresh-access-token",
     * @param {string} OTP - "api/auth/otp/",
     * @param {string} VERIFY_PASSWORD - "api/auth/verify-password"
    */
    static endpoints = {
        LOGIN: "api/auth/login/",
        REGISTER: "api/auth/signup/",
        REFRESH_ACCESS_TOKEN: "api/auth/refresh-access-token/",
        OTP: "api/auth/otp/",
        VERIFY_PASSWORD: "api/auth/verify-password"
    };
}

export default UrlsConfig;
