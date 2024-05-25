import React, {useState, useEffect} from 'react';
import { useAuth } from './AuthContext';
import { ROUTES } from '../../../utils/Pages/RoutesConfig';
import TimedBackdrop from '../Backdrops/TimedBackdrop';
import Layout from '../Layout/Layout';
import ErrorPage from '../../../pages/ErrorPage/ErrorPage';

/**
 * ProtectedRoute component is a higher order component that checks if the user is authenticated before rendering the page.
 * If the user is not authenticated, the user is an error page is rendered with a 401 error message.
 * Example usage:    
 * <Route path={ROUTES.ANALYZE} element={<ProtectedRoute element={<Layout><AnalyzePage /></Layout>} />} />
 * @param {object} Page element to be rendered if authenticated 
 * @returns 
 */
const ProtectedRoute = ({ element }) => {
    const { checkIsAuthenticated } = useAuth();
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        const authStatus = checkIsAuthenticated();
        setIsAuthenticated(authStatus);
    }, [checkIsAuthenticated]);

    if (isAuthenticated === null) {
        // Render the TimedBackdrop while the authentication status is being determined
        return (
            <TimedBackdrop
                duration={1000}
                open={true}
                onClose={() => {}}
            />
        );
    }

    return isAuthenticated ? element : 
    <Layout>
        <ErrorPage errorCode='401' 
        errorMessage='Your login session has expired, please re-login again' 
        redirectToPage={ROUTES.ACCOUNT_PORTAL}>
        </ErrorPage>
    </Layout>;
  };
  
  export default ProtectedRoute;