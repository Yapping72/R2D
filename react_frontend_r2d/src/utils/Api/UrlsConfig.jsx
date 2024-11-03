/**
 * Backend Django API endpoints
 * @param {string} BaseUrl - "http://localhost:8000/"
 * @param {string} LOGIN - "api/auth/login/",
 * @param {string} REGISTER - "api/auth/signup/",
 * @param {string} REFRESH_ACCESS_TOKEN - "api/auth/refresh-access-token",
 * @param {string} OTP - "api/auth/otp/",
 * @param {string} VERIFY_PASSWORD - "api/auth/verify-password"
 * @param {string} CREATE_JOB - "api/jobs/save/"
 * @param {string} GET_ALL_JOBS - "api/jobs/get-all-jobs/"
 * @param {string} GET_JOB_HISTORY - "api/jobs/get-job-history/"
 **/
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
     * @param {string} CREATE_JOB - "api/jobs/save/"
     * @param {string} GET_ALL_JOBS - "api/jobs/get-all-jobs/"
     * @param {string} GET_JOB_HISTORY - "api/jobs/get-job-history/"
    */
    static endpoints = {
        LOGIN: "api/auth/login/",
        REGISTER: "api/auth/signup/",
        REFRESH_ACCESS_TOKEN: "api/auth/refresh-access-token/",
        OTP: "api/auth/otp/",
        VERIFY_PASSWORD: "api/auth/verify-password",
        CREATE_JOB: "api/jobs/save/",
        UPDATE_JOB_STATUS: "api/jobs/update/",
        GET_ALL_JOBS: "api/jobs/get-all-jobs/",
        GET_JOB_HISTORY: "api/jobs/get-job-history/",
    };
}

export default UrlsConfig;
