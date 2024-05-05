
/**
 * GenericQueueRepository class that provides basic CRUD functions
 * for interacting with an IndexedDB object store. This is an abstract
 * class, and concrete implementations should implement handlers for
 * each CRUD operation as needed (e.g., handleFindById, handleAddJobToQueue, etc.).
 */
export class GenericQueueRepository {
    constructor(dbName = "r2d-job-db", storeName) {
        this.dbName = dbName; // Name of the IndexedDB database
        this.storeName = storeName; // Name of the object store within the database
        this.dbVersion = 1; // Update this version whenever a new store is added or schema changes
    }

    /**
    * Opens a connection to the IndexedDB database. 
    * If the database or object store does not exist, they are created.
    * When onboarding new stores to the database they must be added here
    */
    async openDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                // Create all required object stores here - onboard new stores here 
                if (!db.objectStoreNames.contains("user-story-job-queue-store")) {
                    db.createObjectStore("user-story-job-queue-store", { keyPath: "job_id" });
                }
            };
            request.onerror = (event) => reject(event.target.error);
            request.onsuccess = (event) => resolve(event.target.result);
        });
    }

    /**
     * Initializes a transaction and returns the object store for performing operations.
     * @param {string} mode The transaction mode ("readonly" or "readwrite").
     */
    async initTransactionAndStore(mode = "readonly") {
        const db = await this.openDB();
        const transaction = db.transaction([this.storeName], mode);
        const store = transaction.objectStore(this.storeName);
        return store;
    }

    /**
     * Finds a record by its ID.
     * @param {number} id The ID of the record to find.
     */
    async findById(id) {
        const store = await this.initTransactionAndStore("readonly");

        return new Promise((resolve, reject) => {
            const request = store.get(id);
            request.onerror = (event) => reject(event.target.error);
            request.onsuccess = () => resolve(request.result);
        });
    }

    /**
     * Adds Job to Queue Store
     * @param {Object} job job parameter information 
     * Returns the job id added to queue.
     */
    async addJobToQueue(job) {
        const store = await this.initTransactionAndStore("readwrite");
        return new Promise((resolve, reject) => {
            // Combine metadata with the file content
            const request = store.add(job);
            request.onerror = event => reject(event.target.error);
            request.onsuccess = (event) => {
                // Return the id of the added job record
                const id = event.target.result;
                resolve(id);  // Use resolve to return the ID correctly
            };
        });
    }
    /** 
    * Reads all records from the object store.
    * @returns {Promise} A Promise that resolves with an array of all records.
    */
    async readAll() {
        const store = await this.initTransactionAndStore("readonly");
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onerror = (event) => reject(event.target.error);
            request.onsuccess = () => resolve(request.result);
        });
    }
    /**
    * Deletes a record by its ID.
    * @param {number} id The ID of the record to delete.
    */
    async deleteById(id) {
        const store = await this.initTransactionAndStore("readwrite");

        return new Promise((resolve, reject) => {
            const request = store.delete(id);
            request.onerror = (event) => reject(event.target.error);
            request.onsuccess = () => resolve(true);
        });
    }

    /**<ClearDB>
       * Clears all records from the object store.
       * @returns {Promise} A Promise that resolves with true if the operation was successful.
       */
    async clearDB() {
        const store = await this.initTransactionAndStore("readwrite");
        return new Promise((resolve, reject) => {
            const request = store.clear();
            request.onerror = (event) => reject(event.target.error);
            request.onsuccess = () => resolve(true);
        });
    }

    /**
     * Updates the status of a job in the queue store by its ID.
     * @param {string} id The ID of the job whose status is to be updated.
     * @param {string} validNewStatus The new status to be set for the job. This field should be validated before passing
     * @returns {Promise} A Promise that resolves with the new updated record
     */
    async updateJobStatusAndDetailsById(id, validNewStatus="NO STATUS PROVIDED", validJobDetails="NO JOB DETAILS PROVIDED") {
        const store = await this.initTransactionAndStore("readwrite");

        return new Promise((resolve, reject) => {
            const getJobRequest = store.get(id);
            console.debug(getJobRequest);

            getJobRequest.onerror = (event) => {
                console.error("Failed to retrieve job for status update:", event.target.error);
                reject(event.target.error);
            };

            getJobRequest.onsuccess = () => {
                const data = getJobRequest.result;
                // If no job is found with the given ID, reject the promise
                if (!data) {
                    reject(new Error("No job found with the specified ID."));
                    return;
                }

                // Update the job status 
                const updatedData = { ...data, job_status: validNewStatus, job_details: validJobDetails,last_updated_timestamp: new Date().toISOString() };

                // Update the job in the store
                const updateRequest = store.put(updatedData);
                updateRequest.onerror = (event) => {
                    console.error("Failed to update the job status:", event.target.error);
                    reject(event.target.error);
                };
                updateRequest.onsuccess = () => {
                    console.debug(`Job status for ${id} updated successfully to ${validNewStatus}.`);
                    resolve(id);  // Return the job ID after a successful update
                };
            };
        });
    }
}