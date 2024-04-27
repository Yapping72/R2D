export class GenericQueueRepository {
    constructor(dbName, storeName) {
        this.dbName = dbName; // Name of the IndexedDB database
        this.storeName = storeName; // Name of the object store within the database
    }
   
    /**
     * Opens a connection to the IndexedDB database. If the database or object store does not exist, they are created.
     */
    async openDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, 1);

            request.onupgradeneeded = (event) => {
                // Create the object store if it does not exist
                const db = event.target.result;
                if (!db.objectStoreNames.contains(this.storeName)) {
                    db.createObjectStore(this.storeName, { keyPath: "id", autoIncrement: true });
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