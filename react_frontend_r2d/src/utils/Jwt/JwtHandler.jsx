import jwtDecode from 'jwt-decode';

class JwtHandler {
    static getToken() {
        return localStorage.getItem('access-token');
    }

    static setToken(token) {
        localStorage.setItem('access-token', token);
    }

    static clearToken() {
        localStorage.removeItem('access-token');
    }

    static decodeToken() {
        const token = JwtHandler.getToken();
        if (!token) return null;

        try {
            return jwtDecode(token);
        } catch (error) {
            console.error("Failed to decode token:", error);
            return null;
        }
    }

    static getUserClaims() {
        const decodedToken = JwtHandler.decodeToken();
        return decodedToken ? decodedToken : null;
    }
}
export default JwtHandler;
