/**
 * A generic class for interacting with IndexedDB. It provides a set of utility functions to open a database,
 * initialize transactions, and perform CRUD operations on the specified object store within the database.
 */

export class GenericIndexedDBRepository {
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
     * Writes data to the database.
     * @param {*} data The data to be written to the database.
     */
    async writeToDb(data) {
        const store = await this.initTransactionAndStore("readwrite");

        return new Promise((resolve, reject) => {
            const request = store.add(data);
            request.onerror = (event) => reject(event.target.error);
            request.onsuccess = () => resolve(request.result);
        });
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
     * Reads all files stored in the database.
     */
    async readAllFiles() {
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
            request.onsuccess = () => resolve(request.result);
        });
    }

    /**
     * Clears all data from the database.
     */
    async clearDB() {
        const store = await this.initTransactionAndStore("readwrite");

        return new Promise((resolve, reject) => {
            const request = store.clear();
            request.onerror = (event) => reject(event.target.error);
            request.onsuccess = () => resolve(true);
        });
    }
}
