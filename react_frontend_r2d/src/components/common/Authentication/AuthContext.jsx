import React, { createContext, useState, useEffect, useContext, useCallback, useRef } from 'react';
import JwtHandler from '../../../utils/Jwt/JwtHandler';
import { ROUTES } from '../../../utils/Pages/RoutesConfig';
import { PageNavigationService } from '../../../utils/Pages/PageNavigationService';
import useSilentRefresh from './SilentRefreshTimer';
import useIdleTimeout from './useIdleTimeout';
import { WARNING_TIMEOUT, IDLE_TIMEOUT_MS } from '../../../utils/Jwt/TokenConstants';

// Create the context to be used across the application
const AuthContext = createContext();

// Create the AuthProvider component to wrap the application
export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const { navigateTo } = PageNavigationService();
    const [showDialog, setShowDialog] = useState(false);
    const [remainingTime, setRemainingTime] = useState(0);
    const timerRef = useRef(null);

    // Function to handle the idle prompt
    const handleIdlePrompt = useCallback(() => {
        setShowDialog(true);
        setRemainingTime(WARNING_TIMEOUT / 1000);
        if (timerRef.current) {
            clearInterval(timerRef.current);
        }
        timerRef.current = setInterval(() => {
            setRemainingTime(prev => {
                if (prev <= 1) {
                    clearInterval(timerRef.current);
                    timerRef.current = null;
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
    }, []);

    //  Function to handle the logout flow
    const logout = useCallback(() => {
        setIsLoggedIn(false);
        JwtHandler.clearToken();
        navigateTo(ROUTES.HOME);
        idleTimer.reset(); 
        idleTimer.pause();
    }, [navigateTo]);

    // Custom hook to handle user idle timeout
    const idleTimer = useIdleTimeout({
        onIdle: handleIdlePrompt,
        idleTime: IDLE_TIMEOUT_MS,
        logout: logout
    });

    // Idle timeout dialog handler
    const handleStayLoggedIn = useCallback(() => {
        idleTimer.activate();
        setShowDialog(false);
        if (timerRef.current) {
            clearInterval(timerRef.current);
            timerRef.current = null;
        }
        console.debug("User chose to stay logged in");
    }, [idleTimer]);

    const {startSilentRefreshTimer} = useSilentRefresh(logout);

    const checkIsAuthenticated = useCallback(() => {
        if (JwtHandler.checkLocalStorage() && !JwtHandler.isTokenExpired()) {
            setIsAuthenticated(true);
            return true;
        } else {
            setIsAuthenticated(false);
            setIsLoggedIn(false);
            JwtHandler.clearToken();
            return false;
        }
    }, []);

    const setLoginAndSilentRefreshTimer = () => {
        setIsLoggedIn(true);
        startSilentRefreshTimer(); 
        idleTimer.reset();
        idleTimer.start();
    }

    useEffect(() => {
        const isAuth = checkIsAuthenticated();
        if (isAuth) {
            setIsLoggedIn(true);
            setIsAuthenticated(true);
            startSilentRefreshTimer();
        } else {
            setIsLoggedIn(false);
            setIsAuthenticated(false);
        }
    }, []);

    return (
        <AuthContext.Provider value={{ isLoggedIn, isAuthenticated, setLoginAndSilentRefreshTimer, checkIsAuthenticated, logout, showDialog, setShowDialog, remainingTime, handleStayLoggedIn }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};