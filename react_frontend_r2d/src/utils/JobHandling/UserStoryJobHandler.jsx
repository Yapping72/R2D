import GenericJobHandler from "./GenericJobHandler";
import UserStoryJobValidator from "../Validators/UserStoryJobValidator";
import UserStoryJobSanitizer from "../Sanitizers/UserStoryJobSanitizer";

/**
 * UserStoryJobHandler, instantiates the validators, sanitizers and repository classes
 * 
 */
class UserStoryJobHandler extends GenericJobHandler {
    constructor(data) {
        super(new UserStoryJobValidator(data),new UserStoryJobSanitizer(data),  null); // Pass an instance of UserStoryJobValidator
    }

    /**
    * Performs validation and sanitization to populate the job parameters based on the provided data.
    * @param {object} data - The data to populate the job parameters.
    * @throws {Error} Throws an error if data sanitization or validation fails.
    */
     populateJobParameters(data) {
        let validatedData;
        let sanitizedData;

        try {
            // Retrieve validated job parameters
            validatedData = this.validator.validate(data);
            console.debug("User story job data validated");
            console.debug(validatedData);
        } catch (error) {
            console.error("Failed to validate user story job data", error);
            throw new Error("Failed to validate user story job data", error);
        }
        try {
            // Retrieve the sanitized job parameters
            sanitizedData = this.sanitizer.getSanitizedData(validatedData); // Returns features, 
            console.debug("User story job data sanitized");
            // Assign values to job dictionary
            this.job.token_count = sanitizedData.token_count;
            this.job.parameters = sanitizedData;
            console.debug("User Story Job Data: ", this.job);
        } catch (error) {
            console.error("Failed to sanitize user story job data", error);
            throw new Error("Failed to sanitize user story job data", error);
        }
    }
}

export default UserStoryJobHandler