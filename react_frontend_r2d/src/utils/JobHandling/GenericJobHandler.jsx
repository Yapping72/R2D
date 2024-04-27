import { v4 as uuidv4 } from 'uuid';
import GenericJobSanitizer from '../Sanitizers/GenericJobSanitizer';
import GenericJobValidator from '../Validators/GenericJobValidator';

class GenericJobHandler {
    /**
     * @param {object} jobParameterValidator - Object responsible for parsing and validating job parameters.
     * @param {object} jobParameterSanitizer - Object responsible for sanitizing job parameters.
     * @param {object} jobQueueRepository - Object responsible for managing the job queue.
     */
    constructor(jobParameterValidator = new GenericJobValidator(), jobParameterSanitizer = new GenericJobSanitizer(), jobQueueRepository = "") {
        this.validator = jobParameterValidator; // Parse and validate inputs
        this.sanitizer = jobParameterSanitizer; // Sanitize validated inputs
        this.repository = jobQueueRepository; // Queues successfully validated parameters 
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

    /**
     * Helper function to update job status
     * @param {string} jobStatus - The new status of the job
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
        //TBC
        throw new Error("Method 'populateJobParameters' must be implemented by subclass");
    }

    addJobToQueue() {
        //TBC
        console.debug("Adding to queue");
    }

    removeJobFromQueue() {
        //TBC
        console.debug("Remove from queue");
    }
}
export default GenericJobHandler;