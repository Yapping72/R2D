import { v4 as uuidv4 } from 'uuid';
import GenericJobSanitizer from '../Sanitizers/GenericJobSanitizer';
import GenericJobValidator from '../Validators/GenericJobValidator';

class GenericJobHandler {
    /**
     * @param {object} jobParameterValidator - Object responsible for parsing and validating job parameters.
     * @param {object} jobParameterSanitizer - Object responsible for sanitizing job parameters.
     * @param {object} jobQueueRepository - Object responsible for managing the job queue.
     */
    constructor(jobParameterValidator = new GenericJobValidator(), jobParameterSanitizer = new GenericJobSanitizer(), jobQueueRepository="") {
        this.validator = jobParameterValidator; // Parse and validate inputs
        this.sanitizer = jobParameterSanitizer; // Sanitize validated inputs
        this.repository = jobQueueRepository; // Queues successfully validated parameters 
        this.validJobStatus = ["DRAFT", "QUEUED", "SUBMITTED", "ERROR_FAILED_TO_SUBMIT", "PROCESSING", "COMPLETED"]; 
        this.job = [
            {
                "job_id": uuidv4(),
                "user_id": "immutable-user-uuid",
                "job_status": "DRAFT",
                "job_details": "",
                "token_count": 0,
                "job_parameters": [],
                "created_timestamp": Date.now(),
                "last_updated_timestamp": Date.now(),
            }
        ];
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
     * @param {string} job_status - The new status of the job
     */
    updateJobStatus(job_status) {
        if (!this.validJobStatus.includes(job_status)) {
            throw new Error("Invalid job status");
        } else {
            this.job.job_status = job_status;
        }
    }
     /**
     * Populates the job parameters based on the provided data.
     * @param {object} data - The data to populate the job parameters.
     * @throws {Error} Throws an error if data sanitization or validation fails.
     */
    populateJobParameters(data) {
        let validatedData;
        let sanitizedData;

        try {
            validatedData = this.validator.validate(data);
            console.debug("Data passed validation");
            console.debug(validatedData);
            this.job.job_parameters = validatedData;
            console.debug(this.job);
        } catch (error) {
            console.error("Failed to validate input data", error);
            throw new Error("Failed to validate data", error);
        }

        try {
            sanitizedData = this.sanitizer.getSanitizedData(validatedData);
            console.debug("Data successfully sanitized");
            console.debug(sanitizedData);
        } catch (error) {
            console.error("Failed to sanitize input data", error);
            throw new Error("Failed to sanitize data", error);
        }

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