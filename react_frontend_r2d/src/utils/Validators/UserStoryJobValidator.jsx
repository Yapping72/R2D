// UserStoryJobValidator.js
import GenericJobValidator from "./GenericJobValidator";
import { MAX_USER_STORY_FEATURE_LENGTH, MAX_USER_STORY_SUB_FEATURE_LENGTH, MAX_USER_STORY_REQUIREMENT_LENGTH, MAX_USER_STORY_ACCEPTANCE_CRITERIA_LENGTH, MAX_USER_STORY_ADDITIONAL_INFORMATION_LENGTH, MAX_SERVICE_TO_USE_ENTRY_LENGTH, MAX_SERVICES_TO_USE, MAX_USER_STORY_ID_LENGTH} from "./ValidationConstants";

class UserStoryJobValidator extends GenericJobValidator {
    constructor() {
        super(); // Call the constructor of the parent class
        this.features = new Set(); // Stores all features encountered
        this.subFeatures = new Set(); // Stores all sub_features encountered
        this.tokenCount = 0;
        this.jobParameters = {};
    }

    /**
    * Counts the words present in acceptance_criteria, additional_information, requirement,
    * and services_to_use (if available).
    * These fields will be sent for LLM analysis and thus serve as an estimation.
    * @param {object} feature - The feature object containing the fields to count.
    * Returns number of tokens in acceptance_criteria, additional_information, requirement,
    * and services_to_use (if available). 
    */
    countTokens(feature) {
        let totalWordCount = 0; // Initialize total word count
        // Count words in fields like acceptance_criteria, additional_information, and requirement
        const fieldsToCount = ['acceptance_criteria', 'additional_information', 'requirement'];
        fieldsToCount.forEach(field => {
            const fieldValue = feature[field];
            if (fieldValue) {
                const wordCount = fieldValue.split(/\s+/).length;
                console.log(`Word count in ${field}: ${wordCount}`);
                totalWordCount += wordCount; // Add word count to total
            } else {
                console.log(`${field} is missing in the feature.`);
            }
        });

        // Count words in services_to_use if available
        const servicesToUse = feature['services_to_use'];
        if (servicesToUse && Array.isArray(servicesToUse)) {
            const servicesToUseWordCount = servicesToUse.reduce((total, service) => {
                return total + service.split(/\s+/).length;
            }, 0);
            console.log(`Word count in services_to_use: ${servicesToUseWordCount}`);
            totalWordCount += servicesToUseWordCount; // Add word count to total
        } else {
            console.log(`No services to use provided`);
        }
        return totalWordCount; // Return the total word count
    }

    /**
     * Parses the provided data and constructs job parameters in the form of a nested dictionary structure.
     * Each feature is mapped to its respective sub-features, and each sub-feature contains a collection
     * of user story records.
     * 
     * Also performs size validation and ensures all jobParameters loaded meets size constraints.
     * @param {Array} data - An array of objects representing the data to be parsed. Each object should contain
     *                       information about features, sub-features, and user story records.
     * @returns {void}
     * 
     * @example
     * // Input data structure
     * const data = [
     *   {
     *     feature: 'Archival and Disposal',
     *     sub_feature: 'Database Archival',
     *     id: 'Apollo-21',
     *     requirement: 'As a system administrator, I want to archive historical data from the database, so that I can optimize database performance and reduce storage costs.',
     *     services_to_use: ['Amazon S3', 'AWS Glue'],
     *     acceptance_criteria: 'Archived data should be stored in a secure and durable storage solution such as Amazon S3. Archival process should be automated and configurable.',
     *     additional_information: 'Consider data retention policies and regulatory requirements when defining archival criteria.'
     *   },
     * ];
     * 
     * // Converted job parameters structure
     * const job_parameters = {
     *   "Archival and Disposal": {
     *     "Database Archival": {
     *       "Apollo-21": {
     *         "id": "Apollo-21",
     *         "requirement": "As a system administrator, I want to archive historical data from the database, so that I can optimize database performance and reduce storage costs.",
     *         "services_to_use": ["Amazon S3", "AWS Glue"],
     *         "acceptance_criteria": "Archived data should be stored in a secure and durable storage solution such as Amazon S3. Archival process should be automated and configurable.",
     *         "additional_information": "Consider data retention policies and regulatory requirements when defining archival criteria."
     *       }
     *     }
     *   },
     *  
     * };
     */
    parseAndValidateLength(data) {
        data.forEach(item => {
            // Merge features into the feature set
            item.fileMetadata.features.forEach(feature => {
                const validatedFeature = this.validateAndTrim(feature, MAX_USER_STORY_FEATURE_LENGTH);
                if (validatedFeature.length > 0) {
                    this.features.add(validatedFeature); 
                }
            });

            // Merge sub-features into the sub_feature set
            item.fileMetadata['sub features'].forEach(subFeature => {
                const validatedSubFeature = this.validateAndTrim(subFeature, MAX_USER_STORY_SUB_FEATURE_LENGTH);
                if (validatedSubFeature.length > 0) {
                    this.subFeatures.add(validatedSubFeature);
                }
            });
        
            // Retrieve feature data
            item.featureData.forEach(feature => {
                // Check if feature.feature is empty
                if (!feature.feature || feature.feature.trim() === '') {
                    console.warn(`Skipping record because empty feature detected`);
                    return; // Skip this record
                }

                const featureName = this.validateAndTrim(feature.feature, MAX_USER_STORY_FEATURE_LENGTH);

                // Initialize the feature object if it doesn't exist or is not an object
                if (!this.jobParameters[featureName] || typeof this.jobParameters[featureName] !== 'object') {
                    this.jobParameters[featureName] = {};
                }

                // Initialize the subFeature object if it doesn't exist or is not an object
                const subFeatureName = this.validateAndTrim(feature.sub_feature, MAX_USER_STORY_SUB_FEATURE_LENGTH) || `Sub Feature`;
                if (!this.jobParameters[featureName][subFeatureName] || typeof this.jobParameters[featureName][subFeatureName] !== 'object') {
                    this.jobParameters[featureName][subFeatureName] = {};
                }
                
                const featureId = this.validateAndTrim(feature.id, MAX_USER_STORY_ID_LENGTH)
                // Ensure each key-value meets their resource constraints
                this.jobParameters[featureName][subFeatureName][featureId] = {
                    id: featureId,
                    requirement: this.validateAndTrim(feature.requirement, MAX_USER_STORY_REQUIREMENT_LENGTH),
                    services_to_use: this.validateAndTrimArray(feature.services_to_use, MAX_SERVICE_TO_USE_ENTRY_LENGTH).slice(0, MAX_SERVICES_TO_USE),
                    acceptance_criteria: this.validateAndTrim(feature.acceptance_criteria, MAX_USER_STORY_ACCEPTANCE_CRITERIA_LENGTH),
                    additional_information: this.validateAndTrim(feature.additional_information, MAX_USER_STORY_ADDITIONAL_INFORMATION_LENGTH),
                };
            })  
        });
        this.jobParameters["features"] = this.features;
        this.jobParameters["sub_features"] = this.subFeatures;
        console.debug("Parsed Data: ", this.jobParameters);
        return this.jobParameters;
    }

    /**
     * Validates the given string and trims it to the specified maximum number of words if it exceeds.
     * @param {string} value - The string value to validate.
     * @param {number} maxWords - The maximum number of words allowed for the string.
     * @returns {string} - The validated and trimmed string.
     */
    validateAndTrim(value, maxWords) {
        if (!value) return ''; // If value is empty, return empty string
        const words = value.trim().split(/\s+/); // Split the string into words
        if (words.length > maxWords) {
            return words.slice(0, maxWords).join(' '); // Trim to maxWords and join back into a string
        }
        return value.trim(); // Return the original string if it doesn't exceed maxWords
    }

    /**
     * Validates the given array of strings and trims each string to the specified maximum number of words if it exceeds.
     * @param {string[]} array - The array of strings to validate.
     * @param {number} maxWords - The maximum number of words allowed for each string in the array.
     * @returns {string[]} - The validated and trimmed array of strings.
     */
    validateAndTrimArray(array, maxWords) {
        if (!Array.isArray(array)) return []; // If not an array, return empty array
        return array.map(item => this.validateAndTrim(item, maxWords));
    }

    /**
     * Validates the user stories and ensures each of the fields provided meets their size constraints
     * @param {*} data 
     * @returns returns a jobParameter dictonary that should be passed for sanitization
     */
    validate(data) {
        this.parseAndValidateLength(data);
        // Add more validation as required
        return this.jobParameters;
    }
}

export default UserStoryJobValidator;
