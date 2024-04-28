import { GenericQueueRepository } from './GenericQueueRepository'

/**
 * Repository class that provides CRUD to 'r2d-job-db' (database) and 'user-story-job-queue-store' (store)
 */
export class UserStoryJobQueueRepository extends GenericQueueRepository {
  constructor() {
    super("r2d-job-db", "user-story-job-queue-store");
  }
  // Writes the actual file and fileMeta to IndexedDb
  async handleAddJobToQueue(job) {
    try {
      const result = await this.addJobToQueue(job);
      console.debug("Successfully added job to queue");
      return { success: true, data: result };
    } catch (error) {
      console.error("Error adding user story job to queue:", error);
      return { success: false, error: error.message };
    }
  }

  // Writes the actual file and fileMeta to IndexedDb
  async handleReadAll() {
    try {
      const result = await this.readAll();
      console.debug(result);
      return { success: true, data: result };
    } catch (error) {
      console.error("Error adding user story job to queue:", error);
      return { success: false, error: error.message };
    }
  }

  async handleFindById(jobId) {
    try{
        const result = await this.findById(jobId)
        // console.log("File and Metadata retrieved:", result);
        return { success: true, data: result};
    } catch(error) {
        console.error("Error retrieving mermaid file from DB: ", error);
        return { success: false, error: error.message };
    }
}


  // Deletes all records from DB
  async handleClearDb() {
    try {
      const result = await this.clearDB()
      return { success: true };
    } catch (error) {
      console.error("Failed to clear IndexedDb file store: ", error)
      return { success: false, error: error.message };
    }
  }
}