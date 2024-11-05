/**
 * RoutesConfig stores the list of valid frontend routes.
 * When new pages are added to the R2D project, they should be added here.
 * @param {string} BASE - '/',
 * @param {string} HOME - '/home',
 * @param {string} UPLOAD - '/upload',
 * @param {string} ANALYZE - '/analyze',
 * @param {string} VISUALIZE - '/visualize',
 * @param {string} ACCOUNT_PORTAL - '/account-portal', // Login & registration form.
 * @param {string} OTP - '/otp',
 * @param {string} ERROR - '*'
 */
export const ROUTES = {
    BASE: '/',
    HOME: '/home',
    UPLOAD: '/upload',
    ANALYZE: '/analyze',
    VISUALIZE: '/visualize',
    ACCOUNT_PORTAL: '/account-portal', // Login & registration form.
    OTP: '/otp',
    LOGOUT: 'logout',
    HISTORY: '/history',
    ERROR:'*'
};

/**
 * validPaths contains all the route paths from ROUTES for easy validation or iteration.
 * This array is automatically updated as ROUTES changes.
 */
export const validPaths = Object.values(ROUTES);
