import { jwtDecode } from 'jwt-decode';
import ApiManager from '../Api/ApiManager';
import UrlsConfig from '../Api/UrlsConfig';
import { ROUTES } from '../Pages/RoutesConfig';

/**
 * A utility class for handling JSON Web Tokens (JWT) in local storage.
 */
class JwtHandler {
    /**
     * Retrieves the JWT token from local storage.
     * @returns {string|null} The JWT token if present, otherwise null.
     */
    static getToken() {
        return localStorage.getItem('r2d_access_token');
    }

    /**
     * Saves a JWT token to local storage.
     * @param {string} token - The JWT token to be stored.
     */
    static setToken(token) {
        localStorage.setItem('r2d_access_token', token);
    }

    /**
     * Clears the JWT token from local storage.
     */
    static clearToken() {
        localStorage.removeItem('r2d_access_token');
    }

    /**
     * Checks if a JWT token is present in local storage.
     * @returns {boolean} True if a JWT token is present, otherwise false.
     */
    static checkLocalStorage() {
        return localStorage.getItem('r2d_access_token') !== null;
    }

    /**
    * Decodes the JWT token from local storage.
    * @returns {object|null} The decoded JWT token payload if present, otherwise null.
    */
    static decodeToken() {
        const token = JwtHandler.getToken();
        if (token) {
            try {
                return jwtDecode(token);
            } catch (error) {
                console.error('Failed to decode JWT token:', error);
                return null;
            }
        }
        return null;
    }

    /**
    * Helper function to check if the current access token in local storage has expired
    * @returns {bool} True or False denoting if access token has expired. 
    */
    static isTokenExpired() {
        const decodedToken = JwtHandler.decodeToken();
        if (decodedToken) {
            const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
            return decodedToken.exp < currentTime;
        }
        return true; // Return true if there is no token or if it couldn't be decoded
    }

    /**
     * Helper function that to refresh an access token.
     * @returns 
     */
    static async refreshToken() {
        const token = JwtHandler.getToken();
        if (!token || JwtHandler.isTokenExpired) {
            console.debug("Token could not be refreshed as it does not exists, or has already expired")
            return false
        }

        try {
            const requestPayload = {} // Refresh token endpoint does not require a pay
            result = await ApiManager.postData(UrlsConfig.endpoints.REFRESH_ACCESS_TOKEN, requestPayload)
            if (result.success) {
                console.log(`Successfully Refreshed Access Token: ${result.data.access_token}`)
                JwtHandler.setToken(result.data.access_token)
                return true
            }
        } catch (error) {
            console.error('Failed to refresh JWT token:', error);
            return false;
        }

        return false;
    }
}

export default JwtHandler;