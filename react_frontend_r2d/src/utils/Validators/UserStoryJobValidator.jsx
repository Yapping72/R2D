// UserStoryJobValidator.js
import GenericJobValidator from "./GenericJobValidator";
import { MAX_USER_STORY_FEATURE_LENGTH, MAX_USER_STORY_SUB_FEATURE_LENGTH, MAX_USER_STORY_REQUIREMENT_LENGTH, MAX_USER_STORY_ACCEPTANCE_CRITERIA_LENGTH, MAX_USER_STORY_ADDITIONAL_INFORMATION_LENGTH, MAX_SERVICE_TO_USE_ENTRY_LENGTH, MAX_SERVICES_TO_USE, MAX_USER_STORY_ID_LENGTH} from "./ValidationConstants";

class UserStoryJobValidator extends GenericJobValidator {
    constructor() {
        super(); // Call the constructor of the parent class
        this.features = new Set(); // Stores all features encountered
        this.subFeatures = new Set(); // Stores all sub_features encountered
        this.tokens = 0;
        this.jobParameters = {};
        this.validatedParameters = {};
        this.featureMapping = {};
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
     **/

    parseAndValidateLength(data) {
        data.forEach(item => {    
            // Add each feature information to a job_parameters dictionary
            item.featureData.forEach(feature => {
                // Check if feature.feature is empty
                if (!feature.feature || feature.feature.trim() === '') {
                    console.warn(`Skipping record because empty feature detected`);
                    return; // Skip this record
                }

                // Validate the existing feature name ensuring its not too long 
                const featureName = this.validateAndTrim(feature.feature, MAX_USER_STORY_FEATURE_LENGTH);
                if (featureName.length > 0) {
                    this.features.add(featureName);  // Add to features set
                }

                // Initialize the feature object if it doesn't exist or is not an object
                if (!this.jobParameters[featureName] || typeof this.jobParameters[featureName] !== 'object') {
                    this.jobParameters[featureName] = {};
                }

                // Validate the existing sub feature name ensuring its not too long 
                const subFeatureName = this.validateAndTrim(feature.sub_feature, MAX_USER_STORY_SUB_FEATURE_LENGTH) || `Sub Feature`;
                if (subFeatureName.length > 0) {
                    this.subFeatures.add(subFeatureName); // Add to Sub features set
                }

                // Initialize the subFeature object if it doesn't exist or is not an object
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
        
        this.validatedParameters["features"] = this.features;
        this.validatedParameters["sub_features"] = this.subFeatures;
        this.validatedParameters["job_parameters"]=this.jobParameters;
        console.debug("Validated Data: ", this.validatedParameters);
        return this.validatedParameters;
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
        return this.validatedParameters;
    }
}

export default UserStoryJobValidator;
