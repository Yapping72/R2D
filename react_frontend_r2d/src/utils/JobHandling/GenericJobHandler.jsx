import { v4 as uuidv4 } from 'uuid';
import GenericJobSanitizer from '../Sanitizers/GenericJobSanitizer';
import GenericJobValidator from '../Validators/GenericJobValidator';

class GenericJobHandler {
    /**
     * @param {object} jobParameterValidator - Object responsible for parsing and validating job parameters.
     * @param {object} jobParameterSanitizer - Object responsible for sanitizing job parameters.
     */
    constructor(jobParameterValidator = new GenericJobValidator(), jobParameterSanitizer = new GenericJobSanitizer()) {
        this.validator = jobParameterValidator; // Parse and validate inputs
        this.sanitizer = jobParameterSanitizer; // Sanitize validated inputs

        this.validJobStatus = ["DRAFT", "QUEUED", "SUBMITTED", "ERROR_FAILED_TO_SUBMIT", "PROCESSING", "COMPLETED"];
        this.job = {
            job_id: uuidv4(),
            user_id: "immutable-user-uuid", // Retrieved from JWT or other auth mechanism
            job_status: "DRAFT",
            job_details: "Initial Job Creation",
            token_count: 0,
            parameters: {}, // Fields used for backend processing
            created_timestamp: new Date().toISOString(),
            last_updated_timestamp: new Date().toISOString(),
        };
    }

    /**
     * Updates the token count of the job.
     * @param {number} count - The number of tokens to add to the token count.
     */
    updateTokenCount(count) {
        this.job.token_count = count;
    }

    updateLastUpdateTime() {
        this.job.last_updated_timestamp = new Date().toISOString();
    }
    
    /**
     * Helper function to update job status
     * @param {string} jobStatus - The new status of the job
     * Valid Job Status = ["DRAFT", "QUEUED", "SUBMITTED", "ERROR_FAILED_TO_SUBMIT", "PROCESSING", "COMPLETED"];
     */
    updateJobStatus(jobStatus) {
        if (!this.validJobStatus.includes(jobStatus)) {
            throw new Error("Invalid job status");
        } else {
            this.job.job_status = jobStatus;
        }
    }
    /**
     * Helper function to update job status
     * @param {string} jobDetails - The job details of the job
     */
    updateJobDetails(jobDetails) {
        this.job.job_details = jobDetails;
    }
    
    /**
    * Populates the job parameters based on the provided data.
    * @param {object} data - The data to populate the job parameters.
    * @throws {Error} Throws an error if data sanitization or validation fails.
    */
    populateJobParameters(data) {
        throw new Error("Method 'populateJobParameters' must be implemented by subclass");
    }
    /**
     * Adds job to an IndexedDb Queue
     * This function should also modify the job status accordingly
     */
    addJobToQueue() {
        throw new Error("Method 'addJobFromQueue' must be implemented by subclass");
    }
    
    /**
     * Removes job from an IndexedDb Queue
     * This function should also modify the job status accordingly
     */
    removeJobFromQueue() {
        throw new Error("Method 'removeJobFromQueue' must be implemented by subclass");
    }

    /**
     * Note this may need refactoring to incorporate validation
     * @param {job} job 
     */
    setJob(job) {
        const requiredFields = ['job_id', 'user_id', 'job_status', 'job_details', 'token_count', 'parameters', 'created_timestamp', 'last_updated_timestamp'];
        for (let field of requiredFields) {
            if (job[field] === undefined) {
                throw new Error(`Invalid job format: Missing ${field}`);
            }
        }
        this.job = job; // Assume all validations pass
    }
}
export default GenericJobHandler;