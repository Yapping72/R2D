import AxiosClient from './AxiosClient';
import UrlsConfig from './UrlsConfig';

/**
 * A class to manage API requests using an Axios client instance.
 * The APIManager uses the AxiosClient to make FETCH, PUT, POST, DELETE, GET requests.
 * The AxiosClient defines a standard Request and Response Interceptor.
 * ApiManager propagates errors raised by AxiosClient
 */

class ApiManager {
    /**
     * Fetches data from the specified endpoint using a GET request.
     * @param {string} endpoint - The URL endpoint to fetch data from.
     * @returns {Promise<any>} The response data from the server.
     * @throws Will throw an error if the request fails.
     */
    static async fetchData(endpoint) {
        ApiManager.isValidEndpoint(endpoint);
        try {
            const response = await AxiosClient.get(endpoint);
            return response;
        } catch (error) {
            console.error('Error fetching data:', error, error.data);
            return error.data;
        }
    }

    /**
     * Sends data to the specified endpoint using a POST request.
     * @param {string} endpoint - The URL endpoint to send data to.
     * @param {any} data - The data to be sent to the server.
     * @returns {Promise<any>} The response data from the server.
     * @throws Will throw an error if the request fails.
     */
    static async postData(endpoint, requestPayload) {
        ApiManager.isValidEndpoint(endpoint);
        try {
            const response = await AxiosClient.post(endpoint, requestPayload);
            return response;
        } catch (error) {
            console.error('Error posting data:', error, error.data);
            return error.data;
        }
    }

    /**
     * Updates data at the specified endpoint using a PUT request.
     * @param {string} endpoint - The URL endpoint where data will be updated.
     * @param {any} data - The data to update at the server.
     * @returns {Promise<any>} The response data from the server.
     * @throws Will throw an error if the request fails.
     */
    static async updateData(endpoint, requestPayload) {
        ApiManager.isValidEndpoint(endpoint);
        try {
            const response = await AxiosClient.put(endpoint, requestPayload);
            return response;
        } catch (error) {
            console.error('Error updating data:', error, error.data);
            return error.data;
        }
    }

    /**
     * Deletes data at the specified endpoint using a DELETE request.
     * @param {string} endpoint - The URL endpoint to delete data from.
     * @returns {Promise<any>} The response data from the server.
     * @throws Will throw an error if the request fails.
     */
    static async deleteData(endpoint) {
        ApiManager.isValidEndpoint(endpoint);
        try {
            const response = await AxiosClient.delete(endpoint);
            return response;
        } catch (error) {
            console.error('Error deleting data:', error, error.data);   
            return error.data;  
        }
    }

    /**
     * Validates if the provided endpoint exists in the defined UrlsConfig endpoints.
     * @param {string} endpoint - The endpoint to validate.
     */
    static isValidEndpoint(endpoint) {
        // Check if the endpoint is one of the values in UrlsConfig.endpoints
        const endpointValues = Object.values(UrlsConfig.endpoints);
        if (!endpointValues.includes(endpoint)) {
            throw new Error(`Invalid endpoint: ${endpoint}. Endpoint not found in UrlsConfig.`);
        }
    }
}

export default ApiManager;
