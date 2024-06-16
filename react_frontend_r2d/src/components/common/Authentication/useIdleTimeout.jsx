import { useIdleTimer } from "react-idle-timer";
import { WARNING_TIMEOUT, IDLE_TIMEOUT_MS } from "../../../utils/Jwt/TokenConstants";

/**
 * Custom hook to handle user idle timeout.
 *
 * @param {Function} onIdle - Function to notify the user when idle timeout is close.
 * @param {number} idleTime - Number of seconds to wait before user is logged out.
 * @param {Function} logout - Function to handle user logout.
 */
const useIdleTimeout = ({ onIdle, idleTime, logout = () => {console.debug("Simulating log Out")} }) => { 
    /**
     * Function to handle user idle state.
     * Users are logged out when the handleIdle function is invoked
     */
    const handleIdle = () => {
        console.debug("User has been idle longer than permitted time, logging out.");
        logout();
    };

    /**
     * Creates an Idle Timer instance
     * @param {int} timeout - The time to wait before user is deemed to be inactive in milliseconds
     * @param {int} promptBeforeIdle - The time to wait before user is warned about inactivity in milliseconds
     * @param {Function} onPrompt - Function to notify the user when idle timeout is close.
     * @param {Function} onIdle - Function to handle user idle state.
     * @param {int} debounce - The time to wait before the idle timer is reset in milliseconds
     */
    const idleTimer = useIdleTimer({
        timeout: idleTime || IDLE_TIMEOUT_MS, // 7 minutes
        promptBeforeIdle: WARNING_TIMEOUT, // 1 minute
        onPrompt: onIdle,
        onIdle: handleIdle,
        debounce: 500,
        startManually: true,
    });
    // Return the idleTimer instance
    return idleTimer;
};

export default useIdleTimeout;