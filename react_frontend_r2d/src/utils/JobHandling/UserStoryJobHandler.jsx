import GenericJobHandler, { JobStatus } from "./GenericJobHandler";
import UserStoryJobValidator from "../Validators/UserStoryJobValidator";
import UserStoryJobSanitizer from "../Sanitizers/UserStoryJobSanitizer";
import { UserStoryJobQueueRepository } from "../Repository/UserStoryJobQueueRepository";
import ApiManager from '../../utils/Api/ApiManager';
import UrlsConfig from '../../utils/Api/UrlsConfig';
import {ROUTES} from '../../utils/Pages/RoutesConfig';
import { useAlert } from '../../components/common/Alerts/AlertContext';
import JwtHandler from "../Jwt/JwtHandler";

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
                model_name : "gpt-4-turbo",
                job_type: "class_diagram", // default
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
            // Add two keys to data payload
            const requestPayload = {
                payload: {
                    ...data.data, // Spread the existing properties from data.data
                    user_id: JwtHandler.getUserId(), // Add user_id within payload
                    job_type: "class_diagram", // Add job_type within payload
                    model_name: "gpt-4-turbo" // Add model_name within payload
                }
            };   
 
            var jobSubmittedSuccessfully = false; 

            if ([JobStatus.DRAFT, JobStatus.QUEUED, JobStatus.ERROR_FAILED_TO_SUBMIT, JobStatus.ABORTED, JobStatus.COMPLETED].includes(requestPayload.payload.job_status)) {
                // Update job status only if the job is in DRAFT, QUEUED, ERROR_FAILED_TO_SUBMIT, ABORTED, or COMPLETED state
                requestPayload.payload.job_status = JobStatus.SUBMITTED;
                requestPayload.payload.job_details = "Job Submitted Pending Response";
                try {
                    const result = await ApiManager.postData(UrlsConfig.endpoints.CREATE_JOB, requestPayload);
                    if (result.success) {
                        jobSubmittedSuccessfully = true; // Set to true so that job status will be flipped to submitted
                    } 
                } catch (error) {
                    // Handle unexpected errors
                    console.error('Job Processing Error:', error);
                }
            }

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

    /**
     * Helper function to deletes a nested property within the job dictionary structure and cleans up any empty parent objects.
     * @param {Object} params - The main object containing nested properties.  let parameters = data.data.parameters.job_parameters;
     * @param {string} feature - The first-level key within the params object. 
     * @param {string} subFeature - The second-level key within the feature object.
     * @param {string} recordId - The third-level key within the subFeature object, which is to be deleted.
     */
    deleteNestedProperty(params, feature, subFeature, recordId) {
        if (params[feature] && params[feature][subFeature] && params[feature][subFeature][recordId]) {
            // Delete the specific recordId from subFeature
            delete params[feature][subFeature][recordId];

            // Check if subFeature object is now empty, and if so, delete it
            if (Object.keys(params[feature][subFeature]).length === 0) {
                delete params[feature][subFeature];
                
                // Check if feature object is now empty, and if so, delete it
                if (Object.keys(params[feature]).length === 0) {
                    delete params[feature];
                }
            }
        }
    }
    
    async updateDatabaseWithJobData(data) {
        // Update modified fields
        data.data.last_updated_timestamp = new Date().toISOString();
        const tokens = this.recountTokens(data.data.parameters.job_parameters);
        data.data.tokens = tokens;
        data.data.parameters.tokens = tokens;

        const updatedFeaturesAndSubFeatures = this.extractAllFeaturesAndSubFeatures(data.data.parameters.job_parameters);
        data.data.parameters.features = updatedFeaturesAndSubFeatures.features;
        data.data.parameters.sub_features = updatedFeaturesAndSubFeatures.subFeatures;
        // Propagate changes to database
        return await this.repository.handleUpdateRecordById(data.data);
    }
    /**
     * Updates a user story in a job parameter
     * @param {*} jobIdentifier - identifier for job
     * @param {*} feature  - feature that user story belongs to
     * @param {*} subFeature  - subFeature that user story belongs to
     * @param {*} recordId  - user story id e.g., jira-id or apollo-13
     * @param {*} editedData  - edited user story payload containing acceptance_criteria, additional_information, id, requirement and services_to_use
     * @returns 
     */
    async updateUserStoryInJob(jobIdentifier, feature, subFeature, recordId, editedData) {
        try {
            const newData = {
                acceptance_criteria: editedData.acceptance_criteria || "",
                additional_information: editedData.additional_information || "",
                id: editedData.id || "",
                requirement: editedData.requirement || "",
                services_to_use: editedData.services_to_use || []
            };

            // Retrieve existing job parameters to find the record
            const data = await this.retrieveJobFromQueue(jobIdentifier);

            // Retrieve the job parameters to modify
            let parameters = data.data.parameters.job_parameters;
            
            // Remove the old entry if it exists
            this.deleteNestedProperty(parameters, feature, subFeature, recordId);

            // Handle potential absence of any level in the path
            if (!parameters[editedData.feature]) {
                parameters[editedData.feature] = {};
            }
            if (!parameters[editedData.feature][editedData.sub_feature]) {
                parameters[editedData.feature][editedData.sub_feature] = {};
            }

            parameters[editedData.feature][editedData.sub_feature][editedData.id] = newData;
            const result = await this.updateDatabaseWithJobData(data);
            
            return result;
        } catch (error) {
            console.error("Failed to update user story in job:", error);
            throw new Error("Failed to update user story in job: ", error);
        }
    }
    /**
     * Deletes a user story in a job parameter
     * @param {*} jobIdentifier - identifier for job
     * @param {*} feature  - feature that user story belongs to
     * @param {*} subFeature  - subFeature that user story belongs to
     * @param {*} recordId  - user story id e.g., jira-id or apollo-13
     * @param {*} editedData  - edited user story payload containing acceptance_criteria, additional_information, id, requirement and services_to_use
     * @returns 
     */
    async deleteUserStoryInJob(jobIdentifier, feature, subFeature, recordId) {
        try {
            // Retrieve existing job parameters to find the record
            const data = await this.retrieveJobFromQueue(jobIdentifier);

            // Safely navigate and update the nested structure
            let parameters = data.data.parameters.job_parameters;

            this.deleteNestedProperty(parameters, feature, subFeature, recordId);
            const result = await this.updateDatabaseWithJobData(data);
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
    /**
     * Syncs job data between the server and IndexedDB.
     * @returns {Promise<Object>} - An object indicating the success or failure of the synchronization.
     */
    async syncJobsWithServer() {
        try {
            // Step 1: Fetch jobs from the server
            const serverResponse = await ApiManager.postData(UrlsConfig.endpoints.GET_ALL_JOBS, {});           
            const serverJobs = serverResponse.data.jobs;

            // Step 2: Fetch jobs from IndexedDB
            const localJobs = await this.repository.handleReadAll();

            // Step 3: Compare job IDs and synchronize IndexedDB with server data
            const serverJobIds = new Set(serverJobs.map(job => job.job_id));
            const localJobIds = new Set(localJobs.data.map(job => job.job_id));

              // Step 4: Add missing or update outdated jobs in IndexedDB
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

        for (const serverJob of serverJobs) {
            const matchingLocalJob = localJobs.data.find(localJob => localJob.job_id === serverJob.job_id);

            if (!matchingLocalJob) {
                // Add jobs from the server that are missing in IndexedDB
                await this.repository.handleAddJobToQueue(serverJob, serverJob.job_details);
            } else {
                // Update scenario: if the job exists locally but has an older `last_updated_timestamp`, update it
                const serverUpdatedTime = new Date(serverJob.last_updated_timestamp);
                const localUpdatedTime = new Date(matchingLocalJob.last_updated_timestamp);

                if (serverUpdatedTime > localUpdatedTime) {
                    await this.repository.handleUpdateRecordById(serverJob);
                    console.log(`Updated job ${serverJob.job_id} in IndexedDB to match server data.`);
                }
            }
        }

        // Step 5: Remove outdated jobs from IndexedDB that are not in the server data and are more than 7 days old
        for (const localJob of localJobs.data) {
            const jobCreatedDate = new Date(localJob.last_updated_timestamp);

            if (!serverJobIds.has(localJob.job_id) && jobCreatedDate < sevenDaysAgo) {
                await this.repository.handleDeleteById(localJob.job_id);
                console.log(`Deleted job ${localJob.job_id} from IndexedDB as it is more than 7 days old and not found on the server.`);
            }
        }

            console.log("Synchronization complete: IndexedDB is now up-to-date with server data.");
            return { success: true, message: "Jobs synchronized successfully." };
        } catch (error) {
            console.error("Failed to synchronize jobs with server:", error);
            return { success: false, message: "Failed to synchronize jobs.", error };
        }
    }
}

export default UserStoryJobHandler