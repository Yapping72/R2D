import { useNavigate } from 'react-router-dom';
import { validPaths, ROUTES } from './RoutesConfig';


/**
 * Page navigation service that aids in page navigation
 * @returns navigateTo a function that accepts a path to perform redirection to.
 */
export function PageNavigationService() {
    const navigate = useNavigate();

    const navigateTo = (path) => {
        if (validPaths.includes(path)) {
            navigate(path);
        } else {
            console.error("Attempted to navigate to an invalid or undefined path:", path);
            navigate(ROUTES.ERROR); 
        }
    };

    return {
        navigateTo,
    };
}
