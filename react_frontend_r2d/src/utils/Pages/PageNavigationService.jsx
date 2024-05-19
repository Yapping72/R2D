import { useNavigate } from 'react-router-dom';
import { validPaths, ROUTES } from './RoutesConfig';

/**
 * Page navigation service that aids in page navigation
 * To use this class 
 * @import import {PageNavigationService} from ...
 * @usage const {navigateTo} = PageNavigationService();
 * @returns navigateTo a function that accepts a path and optional state to perform redirection to.
 */

export function PageNavigationService() {
    const navigate = useNavigate();

    const navigateTo = (path, state = {}) => {
        if (validPaths.includes(path)) {
            navigate(path, { state });
        } else {
            console.error("Attempted to navigate to an invalid or undefined path:", path);
            navigate(ROUTES.ERROR, { state });
        }
    };

    return {
        navigateTo,
    };
}
