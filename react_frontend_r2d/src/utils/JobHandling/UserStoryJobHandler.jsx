import GenericJobHandler, { JobStatus } from "./GenericJobHandler";
import UserStoryJobValidator from "../Validators/UserStoryJobValidator";
import UserStoryJobSanitizer from "../Sanitizers/UserStoryJobSanitizer";
import { UserStoryJobQueueRepository } from "../Repository/UserStoryJobQueueRepository";

/**
 * Class responsible for creating jobs and adding / removing them from job queue
 */
class UserStoryJobHandler extends GenericJobHandler {
    constructor(data) {
        super(new UserStoryJobValidator(data), new UserStoryJobSanitizer(data)); 
        this.repository = new UserStoryJobQueueRepository();
    }

    /**
    * Performs validation and sanitization to populate the job parameters based on the provided data.
    * @param {object} data - The data to populate the job parameters.
    * @throws {Error} Throws an error if data sanitization or validation fails.
    */
    populateJobParameters(data) {
        try {
            let validatedData = this.validator.validate(data);
            let sanitizedData = this.sanitizer.getSanitizedData(validatedData);
            this.setJob({
                ...this.job,
                parameters: sanitizedData,
                tokens: sanitizedData.tokens,
                last_updated_timestamp: new Date().toISOString() // Assume validation ensures timestamp is correct
            });
            console.debug("User Story Job Data prepared:", this.job);
        } catch (error) {
            console.error("Error preparing job data:", error);
            throw new Error("Error preparing job data", error);
        }
    }
    /**
     * Adds a job to a queue 
     * @param {object} job expects a job dictionary with the following keys - created_timestamp, job_id, job_status, last_updated_timestamp, parameters, tokens, user_id
     * @param {object} job_status Valid Job Status = ["DRAFT", "QUEUED", "SUBMITTED", "ERROR_FAILED_TO_SUBMIT", "PROCESSING", "COMPLETED"];
     * @Returns either a {sucess:bool, data: ?}
     * 
     * */
    async addJobToQueue() {
        try {
            this.updateJobStatus(JobStatus.QUEUED); // Update status before adding to queue
            this.updateJobDetails(`Pending Submission`);
            const result = await this.repository.handleAddJobToQueue(this.job);
            return result;
        } catch (error) {
            console.error("Failed to add job to queue:", error);
            throw new Error("Failed to add job to queue", error);
        }
    }

    /**
     * 
     * @param {*} job_details 
     */
    removeJobFromQueue(job_id) {
        console.debug("Removing job from queue: ", job_id)
    }
}

export default UserStoryJobHandler