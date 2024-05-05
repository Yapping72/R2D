import { GenericQueueRepository } from './GenericQueueRepository'

/**
 * Repository class that provides CRUD to 'r2d-job-db' (database) and 'user-story-job-queue-store' (store)
 */
export class UserStoryJobQueueRepository extends GenericQueueRepository {
  constructor() {
    super("r2d-job-db", "user-story-job-queue-store");
  }

   /** 
   * Adds a job to the user-story-job-queue-store 
   * @param {Object} job The job object to be added to the queue
   * @returns {Object} An object containing the success status and data or error message
   */
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

/** 
   * Reads all records from the user-story-job-queue-store
   * @returns {Object} An object containing the success status and data or error message
   */
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
  /**
   * Wrapper to retrieve a job by its ID
   * @param {string} jobId The ID of the job to retrieve
   * @returns {Object} An object containing the success status and data or error message
   */
  async handleFindById(jobId) {
    try {
      const result = await this.findById(jobId);
      return { success: true, data: result };
    } catch (error) {
      console.error("Error retrieving mermaid file from DB: ", error);
      return { success: false, error: error.message };
    }
  }
  /** 
   * Deletes a job by its ID
   * @param {string} jobId The ID of the job to delete
   * @returns {Object} An object containing the success status and data or error message
   */
  async handleDeleteById(jobId) {
    try {
      const result = await this.deleteById(jobId);
      return {success: true, data: result};
    } catch (error) {
      console.error(`Error failed to delete ${jobId} from DB: `, error);
      return { success: false, error: error.message };
    }
  }
  /**
   * Updates job status and job details of a particular job
   * @param {string} jobId 
   * @param {string} jobStatus 
   * @param {string} jobDetails 
   * @returns 
   */
  async handleUpdateJobStatusAndDetailsById(jobId, jobStatus, jobDetails) {
    try {
      const result = await this.updateJobStatusAndDetailsById(jobId, jobStatus, jobDetails)
      return {success: true, data: result};
    } catch (error) {
      console.error(`Error failed to delete ${jobId} from DB: `, error);
      return { success: false, error: error.message };
    }
  }
  /**
   * The parameters must contain a key called job_id
   * @param {*} parameters 
   * @returns 
   */
  async handleUpdateRecordById(parameters) {
    try {
      const result = await this.updateRecordById(parameters)
      return {success: true, data: result};
    } catch (error) {
      console.error(`Error failed to delete ${jobId} from DB: `, error);
      return { success: false, error: error.message };
    }
  }

   /**
   * Deletes all records from the r2d-job-db/user-story-job-queue-store
   * @returns {Object} An object containing the success status and error message (if any)
   */
  async handleClearDb() {
    try {
      const result = await this.clearDB()
      return { success: true };
    } catch (error) {
      console.error(`Failed to delete all records from ${this.dbName}-${this.storeName}: `, error)
      return { success: false, error: error.message };
    }
  }
}