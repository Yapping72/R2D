import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import JwtHandler from '../../../utils/Jwt/JwtHandler';

import { ROUTES } from '../../../utils/Pages/RoutesConfig';
import { PageNavigationService } from '../../../utils/Pages/PageNavigationService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [inactivityTimer, setInactivityTimer] = useState(null);
    const { navigateTo } = PageNavigationService();

    const setLoginAndStartInactivityTimer = useCallback(() => {
        console.debug("User logged in")
        setIsLoggedIn(true);
        // Start the inactivity timer when the user logs in
        startInactivityTimer();
    }, []);

    const logout = useCallback(() => {
        console.debug("User logged out")
        setIsLoggedIn(false);
        JwtHandler.clearToken();
        // Clear the inactivity timer when the user logs out
        if (inactivityTimer) {
            clearTimeout(inactivityTimer);
        }
        navigateTo(ROUTES.HOME)
    }, [inactivityTimer]);

    const refreshToken = useCallback(async () => {
        console.debug("Attempting to refresh token")
        const newToken = await JwtHandler.refreshToken();
        if (newToken) {
            // Reset the inactivity timer upon successful token refresh
            startInactivityTimer();
        } else {
            logout(); // Logout if token refresh fails
        }
    }, [logout]);

    const startInactivityTimer = useCallback(() => {
        console.debug("Inactivity timer started")
        if (inactivityTimer) {
            clearTimeout(inactivityTimer);
        }
        // Set the inactivity timer for a duration less than token expiry time (e.g., 10 minutes)
        const timer = setTimeout(() => {
            refreshToken();
        }, 8 * 60 * 1000); // Silently refresh token every 8 minutes (80% of token expiration time)
        setInactivityTimer(timer);
    }, [inactivityTimer, refreshToken]);

    useEffect(() => {
        if (JwtHandler.checkLocalStorage() && !JwtHandler.isTokenExpired()) {
            setLoginAndStartInactivityTimer(); // Automatically log in if there's a valid token in local storage
        }
    }, [setLoginAndStartInactivityTimer]);

    return (
        <AuthContext.Provider value={{ isLoggedIn, setLoginAndStartInactivityTimer, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
