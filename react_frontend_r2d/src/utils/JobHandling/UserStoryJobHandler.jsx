import GenericJobHandler, { JobStatus } from "./GenericJobHandler";
import UserStoryJobValidator from "../Validators/UserStoryJobValidator";
import UserStoryJobSanitizer from "../Sanitizers/UserStoryJobSanitizer";
import { UserStoryJobQueueRepository } from "../Repository/UserStoryJobQueueRepository";

/**
 * Class responsible for managing User Story jobs
 */
class UserStoryJobHandler extends GenericJobHandler {
    constructor() {
        super(new UserStoryJobValidator(), new UserStoryJobSanitizer());
        this.repository = new UserStoryJobQueueRepository();
    }

    /**
    * Performs validation and sanitization to populate the job parameters based on the provided data.
    * Sets this.job to contain the job parameters
    * @param {object} data - The data to populate the job parameters.
    * @throws {Error} Throws an error if data sanitization or validation fails.
    * @returns {object} job - job object
    */
    populateJobParameters(data) {
        try {
            let validatedData = this.validator.validate(data);
            let sanitizedData = this.sanitizer.getSanitizedData(validatedData);
            const job = {
                ...this.job,
                parameters: sanitizedData,
                tokens: sanitizedData.tokens,
                last_updated_timestamp: new Date().toISOString() // Assume validation ensures timestamp is correct
            }
            this.setJob(job);
            console.debug("User Story Job Data prepared:", this.job);
            return job;
        } catch (error) {
            console.error("Error preparing job data:", error);
            throw new Error("Error preparing job data", error);
        }
    }
    /**
     * Adds a job to a queue 
     * @param {object} job expects a job dictionary with the following keys - created_timestamp, job_id, job_status, last_updated_timestamp, parameters, tokens, user_id
     * @param {object} jobStatus Valid Job Status = ["DRAFT", "QUEUED", "SUBMITTED", "ERROR_FAILED_TO_SUBMIT", "PROCESSING", "COMPLETED"];
     * @Returns either a {success:bool, data: ?}
     * 
     * */
    async addJobToQueue(job, jobStatus = JobStatus.QUEUED, jobDetails = "Pending Submission") {
        try {
            this.setJob(job); // sets the current job object to the one provided
            this.updateJobStatus(jobStatus); // Update status before adding to queue
            this.updateJobDetails(jobDetails);
            console.debug(job);
            const result = await this.repository.handleAddJobToQueue(this.job);
            return result;
        } catch (error) {
            console.error("Failed to add job to queue:", error);
            throw new Error("Failed to add job to queue", error);
        }
    }

    /**
     * Deletes a job from the queue
     * @param {integer} jobIdentifier 
     */
    async removeJobFromQueue(jobIdentifier) {
        try {
            const result = await this.repository.handleDeleteById(jobIdentifier);
            return result;
        } catch (error) {
            console.error("Failed to add job to queue:", error);
            throw new Error("Failed to add job to queue", error);
        }
    }
    /**
     * Retrieves job parameters from the job queue
     * @param {integer} jobIdentifier 
     * @returns 
     */
    async retrieveJobFromQueue(jobIdentifier) {
        try {
            const result = await this.repository.handleFindById(jobIdentifier);
            return result;
        } catch (error) {
            console.error("Failed to find job in queue:", error);
            throw new Error("Failed to find job in queue:", error);
        }
    }
    /**
     * Attempts to submit a job and update its status based on the submission result.
     * @param {string} jobIdentifier - The unique identifier for the job to be submitted.
     * @returns {Promise<Object>} - A promise that resolves to an object indicating the success or failure of the operation.
     */
    async submitJob(jobIdentifier) {
        try {
            // Step 1: Retrieve job parameters for the provided job identifier.
            // This includes all necessary data needed to submit the job to the backend.
            const data = await this.retrieveJobFromQueue(jobIdentifier);
            console.debug("Data Retrieved: ", data);

            // TODO:
            // Step 2: Valid job status and parameters
            // 1. Validate job state - job must be in valid job status i.e., one that can be submitted
            // 2. Validate job parameters before sending them out, job parameters should include XXX keys

            // TODO: 
            // Step 3: Send the payload to backend and wait for response 
            const jobSubmittedSuccessfully = false; // Mocked as false to simulate failure.

            // jobSubmittedSuccessfully denotes the backend response 
            if (jobSubmittedSuccessfully) {
                return await this.repository.handleUpdateJobStatusAndDetailsById(jobIdentifier, JobStatus.SUBMITTED, "Job Submitted Pending Response");
            }
            else {
                const result = await this.repository.handleUpdateJobStatusAndDetailsById(jobIdentifier, JobStatus.ERROR_FAILED_TO_SUBMIT, "Failed to submit job");
                return { ...result, success: false };
            }
        } catch (error) {
            console.error("Failed to submit job:", error);
            throw new Error("Failed to submit job", error);
        }
    }
    /**
     * Attempts to abort a job and update its status based on the submission result.
     * @param {string} jobIdentifier - The unique identifier for the job to be submitted.
     * @returns {Promise<Object>} - A promise that resolves to an object indicating the success or failure of the operation.
     */
    async abortJob(jobIdentifier) {
        try {
            // Check that the job status is in PROCESSING
            const data = await this.retrieveJobFromQueue(jobIdentifier);
            if (data.data.job_status != JobStatus.PROCESSING) {
                console.debug("Cannot abort a job not in PROCESSING state")
                return { success: false }
            }
            // TODO: Trigger a backend call to abort / terminate the job
            const jobAbortedSuccessfully = false; // Mocked as false to simulate failure.

            // jobSubmittedSuccessfully denotes the backend response 
            if (jobAbortedSuccessfully) {
                return await this.repository.handleUpdateJobStatusAndDetailsById(jobIdentifier, JobStatus.ABORTED, "Job Aborted");
            }
            else {
                return { ...result, success: false };
            }
        } catch (error) {
            console.error("Failed to abort job:", error);
            throw new Error("Failed to abort job", error);
        }
    }
}

export default UserStoryJobHandler