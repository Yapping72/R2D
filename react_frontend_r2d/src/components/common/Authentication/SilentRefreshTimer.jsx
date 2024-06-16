import { useRef } from 'react';
import JwtHandler from '../../../utils/Jwt/JwtHandler';
import { ACCESS_TOKEN_LIFETIME } from '../../../utils/Jwt/TokenConstants';

/**
 * Silent refresh hook to refresh the token before it expires.
 * The hook starts a timer, when the timer elapses 80% of the access tokens lifetime the token is silently refreshed.
 * @param {function} logout function to invoke logout flow
 * @returns 
 */

const useSilentRefresh = (logout) => {
    const silentRefreshTimerRef = useRef(null);

    const refreshToken = async () => {
        console.debug("Attempting to refresh token");
        const newToken = await JwtHandler.refreshToken();
        if (newToken) {
            startSilentRefreshTimer();
            console.debug("Token refreshed successfully, resetting timer", newToken);
        } else {
            console.error("Failed to refresh token");
            logout(); // Logout if token refresh fails
        }
    };

    const startSilentRefreshTimer = () => {
        if (silentRefreshTimerRef.current) {
            console.debug("Silent refresh timer is already running, skipping start");
            return;
        }

        const interval = (0.8 * ACCESS_TOKEN_LIFETIME) * 60 * 1000; // 80% of token expiration time in milliseconds
        const expirationTime = new Date(Date.now() + interval);

        console.debug(`Starting silent refresh timer with interval of ${interval / 1000} seconds`);
        console.debug(`Silent refresh timer will expire at: ${expirationTime.toLocaleString()}`);

        silentRefreshTimerRef.current = setTimeout(() => {
            console.debug("Silent Refresh Timer Expired");
            refreshToken();
            silentRefreshTimerRef.current = null; // Clear the reference after the timer expires
        }, interval);

        console.debug(`Timer_Id: ${silentRefreshTimerRef.current}, Interval: ${interval}`)
    }

    return {
        startSilentRefreshTimer,
    };
};

export default useSilentRefresh;