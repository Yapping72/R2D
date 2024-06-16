import JwtHandler from "../Jwt/JwtHandler";

/**
 * A generic class for interacting with IndexedDB. It provides a set of utility functions to open a database,
 * initialize transactions, and perform CRUD operations on the specified object store within the database.
 */

export class GenericFileRepository {
    constructor(dbName = "r2d-file-db", storeName, user_id) {
        this.dbName = `${dbName}_${user_id}`; // Name of the IndexedDB database (r2d-file-store) is the default repository to store files to
        this.storeName = storeName; // Name of the object store within the database
        this.dbVersion = 2; // Update this version whenever a new store is added or schema changes
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
                if (!db.objectStoreNames.contains("user-story-file-store")) {
                    db.createObjectStore("user-story-file-store", { keyPath: "id", autoIncrement: true });
                }
                if (!db.objectStoreNames.contains("mermaid-file-store")) {
                    db.createObjectStore("mermaid-file-store", { keyPath: "id", autoIncrement: true });
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
    * Retrieves all records from the specified object store within the database.
    * This method initializes a transaction in "readonly" mode to ensure data integrity and prevent modifications during the read process.
    * It accesses the object store and performs a getAll operation, which fetches every record stored.
    * This operation is typically used for loading an entire dataset into memory when you need to display a list, perform batch operations, or when starting the application and populating initial data.
    * 
    * @returns {Promise<Array>} A promise that resolves with an array of all records in the object store if the operation is successful. 
    * The promise rejects with an error if the operation fails, providing an error message detailing the cause of the failure.
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
     * Writes a file and its metadata to the database.
     * @param {File} file The file to store.
     * @param {Object} metadata Metadata associated with the file.
     */
    async writeFileAndMetadataToDB(file, metadata) {
        const store = await this.initTransactionAndStore("readwrite");
    
        return new Promise((resolve, reject) => {
            // Combine metadata with the file content
            const fileRecord = { ...metadata, content: file };
            const request = store.add(fileRecord);
    
            request.onerror = event => reject(event.target.error);
    
            request.onsuccess = (event) => {
                // Get the generated id from the event
                const id = event.target.result;
                
                // Add the id to your metadata
                const updatedMetadata = { ...metadata, id };
                resolve(updatedMetadata);
            };
        });
    }

    /**
     * Clears all data from the database's specified object store.
     * This method initializes a transaction with "readwrite" permissions,
     * accesses the designated object store, and performs a clear operation.
     * This effectively removes all records within the store, resetting it to an empty state.
     * This operation is useful for situations where you need to purge all existing data,
     * such as resetting the application state or preparing the database for new data after significant schema changes.
     * @returns {Promise<boolean>} A promise that resolves with true if the operation is successful,
     * or rejects with an error if the operation fails.
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
     * Updates a record by its ID.
     * @param {number} id The ID of the record to update.
     * @param {Object} updatedFile The updated record data.
     * @param {Object} updatedFileMetadata Metadata of the updatedfile
     * @returns {Promise<Object>} A promise that resolves with the updated record data or rejects with an error.
     */
    async updateFileAndMetadataToDB(id, updatedFile, updatedFileMetadata) {
        const store = await this.initTransactionAndStore("readwrite");

        return new Promise((resolve, reject) => {
            const fileRecord = { ...updatedFileMetadata, content: updatedFile, id: id };
            const request = store.put(fileRecord);

            request.onerror = (event) => {
                console.error("Error updating record by ID:", event.target.error);
                reject(event.target.error);
            };
    
            request.onsuccess = () => {
                resolve({ ...updatedFile, id });
            };
        });
    }
}
