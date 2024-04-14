import AxiosClient from './AxiosClient';

class ApiManager {
    // GET request
    static async fetchData(endpoint) {
        try {
            const response = await AxiosClient.get(endpoint);
            return response.data;
        } catch (error) {
            // Handle errors or rethrow them to be handled by the caller
            console.error('Error fetching data:', error);
            throw error;
        }
    }

    // POST request
    static async postData(endpoint, data) {
        try {
            const response = await AxiosClient.post(endpoint, data);
            return response.data;
        } catch (error) {
            console.error('Error posting data:', error);
            throw error;
        }
    }

    // PUT request
    static async updateData(endpoint, data) {
        try {
            const response = await AxiosClient.put(endpoint, data);
            return response.data;
        } catch (error) {
            console.error('Error updating data:', error);
            throw error;
        }
    }

    // DELETE request
    static async deleteData(endpoint) {
        try {
            const response = await AxiosClient.delete(endpoint);
            return response.data;
        } catch (error) {
            console.error('Error deleting data:', error);
            throw error;
        }
    }
}

export default ApiManager;
