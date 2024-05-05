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
        console.debug("Attempting to populate job parameters using: ", data);
        try {
            let validatedData = this.validator.validate(data);
            let sanitizedData = this.sanitizer.getSanitizedData(validatedData);
            const job = {
                ...this.job,
                parameters: sanitizedData,
                tokens: sanitizedData.tokens,
                last_updated_timestamp: new Date().toISOString() // Validation ensures timestamp is correct
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

    async updateUserStoryInJob(jobIdentifier, feature, subFeature, recordId, editedData) {
        try {
            const newData = {
                acceptance_criteria: editedData.acceptance_criteria,
                additional_information: editedData.additional_information,
                id: editedData.id,
                requirement: editedData.requirement,
                services_to_use: editedData.services_to_use,
            }

            // Retrieve existing job parameters to find the record
            const data = await this.retrieveJobFromQueue(jobIdentifier);

            // Safely navigate and update the nested structure
            let parameters = data.data.parameters.job_parameters;

            // Remove the old entry if it exists
            if (parameters[feature] && parameters[feature][subFeature] && parameters[feature][subFeature][recordId]) {
                delete parameters[feature][subFeature][recordId];
            }

            // Handle potential absence of any level in the path
            if (!parameters[editedData.feature]) {
                parameters[editedData.feature] = {};
            }
            if (!parameters[editedData.feature][editedData.sub_feature]) {
                parameters[editedData.feature][editedData.sub_feature] = {};
            }

            parameters[editedData.feature][editedData.sub_feature][editedData.id] = newData;

            // Update modified fields before committing to DB
            data.data.last_updated_timestamp = new Date().toISOString();
            const tokens = this.recountTokens(data.data.parameters.job_parameters);
            data.data.tokens = tokens;
            data.data.parameters.tokens = tokens;
            const updatedFeaturesAndSubFeatures = this.extractAllFeaturesAndSubFeatures(data.data.parameters.job_parameters);
            data.data.parameters.features = updatedFeaturesAndSubFeatures.features;
            data.data.parameters.sub_features = updatedFeaturesAndSubFeatures.subFeatures;
            // Propagate changes to database
            const result = await this.repository.handleUpdateRecordById(data.data); 
            return result;
        } catch (error) {
            console.error("Failed to update user story in job:", error);
            throw new Error("Failed to update user story in job: ", error);
        }
    }

    async deleteUserStoryInJob(jobIdentifier, feature, subFeature, recordId) {
        try {
            // Retrieve existing job parameters to find the record
            const data = await this.retrieveJobFromQueue(jobIdentifier);

            // Safely navigate and update the nested structure
            let parameters = data.data.parameters.job_parameters;

            // Remove the old entry if it exists
            if (parameters[feature] && parameters[feature][subFeature] && parameters[feature][subFeature][recordId]) {
                delete parameters[feature][subFeature][recordId];
            }

            // Update modified fields before committing to DB
            data.data.last_updated_timestamp = new Date().toISOString();
            const tokens = this.recountTokens(data.data.parameters.job_parameters);
            data.data.tokens = tokens;
            data.data.parameters.tokens = tokens;
            const updatedFeaturesAndSubFeatures = this.extractAllFeaturesAndSubFeatures(data.data.parameters.job_parameters);
            data.data.parameters.features = updatedFeaturesAndSubFeatures.features; // DEBUG THIS NOT WROKING
            data.data.parameters.sub_features = updatedFeaturesAndSubFeatures.subFeatures;
            console.log(updatedFeaturesAndSubFeatures);
            console.log(data)
            const result = await this.repository.handleUpdateRecordById(data.data); // Propagate changes to database
            return result;
        } catch (error) {
            console.error("Failed to add job to queue:", error);
            throw new Error("Failed to add job to queue", error);
        }
    }

    recountTokens(jsonData) {
        let tokenCount = 0;
    
        // Helper function to count words in a string
        function countWords(str) {
            return str.split(/\s+/).length;
        }
    
        // Recursive function to explore each object or array
        function explore(node) {
            if (typeof node === 'object' && node !== null) {
                for (const key in node) {
                    if (node.hasOwnProperty(key)) {
                        const value = node[key];
                        // Check if the current key is one of the fields we're interested in
                        if (['requirement', 'acceptance_criteria', 'additional_information'].includes(key) && typeof value === 'string') {
                            tokenCount += countWords(value);
                        } else if (key === 'services_to_use' && Array.isArray(value)) {
                            // Count each entry in the services_to_use array as a word
                            tokenCount += value.length;
                        }
    
                        // Recursively explore objects and arrays
                        explore(value);
                    }
                }
            }
        }
        // Start the recursive exploration
        explore(jsonData);
        return tokenCount;
    }

    getFeatures(jsonData) {
        return Object.keys(jsonData);
    }
    
    extractAllFeaturesAndSubFeatures(jsonData) {
        let features = new Set();
        let subFeatures = new Set();
    
        // Iterate over the JSON data to collect features and sub-features
        Object.keys(jsonData).forEach(feature => {
            if (feature === "tokens") {
                return;
            }

            features.add(feature); // Add feature to the set
    
            // Iterate through each sub-feature and add to the subFeatures set
            Object.keys(jsonData[feature]).forEach(subFeature => {
                subFeatures.add(subFeature); // Add sub-feature to the set
            });
        });
    
        return { features: Array.from(features), subFeatures: Array.from(subFeatures) };
    }
}

export default UserStoryJobHandler