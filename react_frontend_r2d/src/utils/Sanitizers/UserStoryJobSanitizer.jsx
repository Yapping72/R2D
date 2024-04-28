import GenericJobSanitizer from './GenericJobSanitizer'

class UserStoryJobSanitizer extends GenericJobSanitizer {
    constructor() {
        super();
        this.sanitizedFeatures = new Set();
        this.sanitizedSubFeatures = new Set();
        this.sanitizedJobParams = {};
        this.tokenCount = 0;
        // Initialize sanitizedData structure; token count and job parameters will be updated after sanitization
        this.sanitizedData = {};
    }

    escapeHTML(input) {
        if (typeof input !== 'string') {
            return '';
        }
        return input.replace(/[&<>"']/g, function (match) {
            switch (match) {
                case '&':
                    return '&amp;';
                case '<':
                    return '&lt;';
                case '>':
                    return '&gt;';
                case '"':
                    return '&quot;';
                case "'":
                    return '&#x27;';
                default:
                    return match;
            }
        });
    }

    /**
    * Counts the words present in acceptance_criteria, additional_information, requirement,
    * and services_to_use (if available).
    * These fields will be sent for LLM analysis and thus serve as an estimation.
    * @param {object} story - A dictionary object containing the following keys: acceptance_criteria, additional_information,requirement, services_to_use
    * Returns number of tokens in the provided dictionary
    */
    countTokens(story) {
        let totalWordCount = 0; // Initialize total word count
        // Count words in fields like acceptance_criteria, additional_information, and requirement
        const fieldsToCount = ['acceptance_criteria', 'additional_information', 'requirement'];
        fieldsToCount.forEach(field => {
            const fieldValue = story[field];
            if (fieldValue) {
                const wordCount = fieldValue.split(/\s+/).length;
                totalWordCount += wordCount; // Add word count to total
            } else {
                console.debug(`${field} is missing in the story.`);
            }
        });

        // Count words in services_to_use if available
        const servicesToUse = story['services_to_use'];
        if (servicesToUse && Array.isArray(servicesToUse)) {
            const servicesToUseWordCount = servicesToUse.reduce((total, service) => {
                return total + service.split(/\s+/).length;
            }, 0);
            totalWordCount += servicesToUseWordCount; // Add word count to total
        } else {
            console.debug(`No services to use provided`);
        }
        console.debug("Word Count: ", totalWordCount);
        return totalWordCount; // Return the total word count
    }

    // Sanitizes the features set 
    // Returns a sanitized feature set
    sanitizeFeatures(features) {
        // TBC in security sprint
        for (const feature of features) {
            // Implement actual sanitization logic here
            const sanitizedFeature = feature;
            this.sanitizedFeatures.add(sanitizedFeature);
        }

        this.sanitizedData["features"] = Array.from(this.sanitizedFeatures);
        return this.sanitizedFeatures;
    }

    // Sanitizes the sub features set
    // Returns a sanitized sub feature set
    sanitizeSubFeatures(subFeatures) {
        // TBC in security sprint
        for (const subFeature of subFeatures) {
            const sanitizedSubFeature = subFeature;
            this.sanitizedSubFeatures.add(sanitizedSubFeature);
        }
        
        this.sanitizedData["sub_features"] = Array.from(this.sanitizedSubFeatures);
        return this.sanitizedSubFeatures;
    }
    // Sanitizes job parameters dictionary
    // Returns a sanitized job parameter dictionary 
    sanitizeJobParameters(jobParameters ) {
        // TBC in security sprint
        for (const featureKey in jobParameters) {
            let sanitizedFeature = jobParameters[featureKey]; // Sanitize Features
            this.sanitizedJobParams[sanitizedFeature] = {}; // Initialize nested object for feature

            console.debug(featureKey, jobParameters[featureKey], sanitizedFeature); 
            for (const subFeatureKey in jobParameters[featureKey]) {
                let sanitizedSubFeature = jobParameters[featureKey][subFeatureKey]; // Sanitize SubFeature
                this.sanitizedJobParams[sanitizedFeature][sanitizedSubFeature] = {}; // Initialize nested object for subFeature
                console.debug(subFeatureKey, jobParameters[featureKey][subFeatureKey], sanitizedSubFeature);
                for (const storyId in jobParameters[featureKey][subFeatureKey]) {
                    let sanitizedStoryId = storyId; // Sanitize This
                    let sanitizedStory = jobParameters[featureKey][subFeatureKey][storyId]; // Sanitize the story - requirement, acceptance_criteria etc.
                    this.tokenCount += this.countTokens(sanitizedStory); // Counts tokens that will be sent for analysis
                    console.debug(storyId, jobParameters[featureKey][subFeatureKey][storyId], sanitizedStory);
                    this.sanitizedJobParams[sanitizedFeature][sanitizedSubFeature][sanitizedStoryId] = sanitizedStory;
                    console.debug("Sanitized Job Parameters: ", this.sanitizedJobParams)
                }   
            }
        }
        
    // Merge this into the existing job_parameters without overwriting
        this.sanitizedData["job_parameters"] = {
            ...this.sanitizedData["job_parameters"],
            ...this.sanitizedJobParams
        };
        this.sanitizedData["tokens"] = this.tokenCount;
        return this.sanitizedData;
    }

    getSanitizedData(data) {
        console.debug("In UserStoryJobSanitizer");
        // Iterate through each key and perform the sanitization
        console.debug(this.sanitizeFeatures(data['features']));
        console.debug(this.sanitizeSubFeatures(data['sub_features']));
        console.debug(this.sanitizeJobParameters(data['job_parameters']));
        return this.sanitizedData;
    }
}

export default UserStoryJobSanitizer;