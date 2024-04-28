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
                // Create all required object stores here 
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
}