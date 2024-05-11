/**
 * RoutesConfig stores the list of valid routes in the application.
 * When new pages are added to the R2D project, they should be added here.
 */
export const ROUTES = {
    BASE: '/',
    HOME: '/home',
    ACCOUNT: '/account-portal',
    UPLOAD: '/upload',
    ANALYZE: '/analyze',
    VISUALIZE: '/visualize',
    ACCOUNT_PORTAL: '/account-portal', // Login & registration form.
    ERROR:'*'
};

/**
 * validPaths contains all the route paths from ROUTES for easy validation or iteration.
 * This array is automatically updated as ROUTES changes.
 */
export const validPaths = Object.values(ROUTES);
