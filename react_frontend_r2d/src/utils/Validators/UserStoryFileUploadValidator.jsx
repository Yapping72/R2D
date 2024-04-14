import FileUploadValidator from "./FileUploadValidator";
import FileReaderUtility from '../FileHandling/FileReaderUtility'

class UserStoryFileUploadValidator extends FileUploadValidator {
    constructor(validExtensions = ['application/json', 'json'], maxFileSize = 15 * 1024 * 1024, maxLineCount = 1000) {
        super(validExtensions, maxFileSize, maxLineCount);
    }

    // Validates that the json contains, feature, sub_feature and requirements
    async validateJsonKeysAndGetMetadata(file) {
        const contentAsString = await FileReaderUtility.readAsText(file);
        const contentAsJson = JSON.parse(contentAsString);

        // Ensure word limits
        const maxWordsFeature = 15; // Example limit for 'feature'
        const maxWordsSubFeature = 15; // Example limit for 'sub_feature'
        const maxWordsRequirement = 300; // Example limit for 'requirement'

        // Perform validation and counting in a single iteration
        // Use Sets to track unique features and sub-features
        const featuresSet = new Set();
        const subFeaturesSet = new Set();
        let totalWordCount = 0;
        let validatedRecords = 0; // Counter for records that pass validation
        let skippedRecords = 0; // Counter for records that are skipped

        // Perform validation and counting in a single iteration
        contentAsJson.forEach(item => {
            // Validation for required keys
            if (!('feature' in item && 'sub_feature' in item && 'requirement' in item)) {
                console.warn(`Item at index ${index} is missing one or more required keys: 'feature', 'sub_feature', 'requirement'.`);
                skippedRecords++;
                return;
            }
            
            if (item.feature.split(/\s+/).length > maxWordsFeature) {
                console.warn(`'feature' field in item at index ${index} exceeds the maximum word count of ${maxWordsFeature}.`);
                skippedRecords++;
                return;
            }
            if (item.sub_feature.split(/\s+/).length > maxWordsSubFeature) {
                console.warn(`'sub_feature' field in item at index ${index} exceeds the maximum word count of ${maxWordsSubFeature}.`);
                skippedRecords++;
                return;
            }
            if (item.requirement.split(/\s+/).length > maxWordsRequirement) {
                console.warn(`'requirement' field in item at index ${index} exceeds the maximum word count of ${maxWordsRequirement}.`);
                skippedRecords++;
                return;
            }
            // Add features and sub-feature IDs to their respective Sets
            featuresSet.add(item.feature);
            subFeaturesSet.add(item.sub_feature);

            // Count words in the requirement
            totalWordCount += item.requirement.split(/\s+/).length;
            validatedRecords++; // Increment validated record counter
        });

    // Check if all records were skipped
    if (validatedRecords === 0) {
        throw new Error("All records were skipped due to validation failures.");
    } else {
        console.log(`Skipped records: ${skippedRecords}. Validated records: ${validatedRecords}/${skippedRecords}`);
    }
    
    // Return the extracted metadata
    return {
        "word count": totalWordCount,
        "features": featuresSet,
        "sub features": subFeaturesSet
    };
    }
    // Performs base file validation
    // Performs additional JSON field validation
    // Returns User Story Metadata
    async validate(file) {
        // Call the base validation first
        const baseValidation = await super.validate(file);
        
        // If base validation fails, return its result immediately
        if (baseValidation.result === 'fail') {
            return baseValidation;
        }

        // Additional JSON-specific validation and metadata extraction
        try {
            const jsonMetadata = await this.validateJsonKeysAndGetMetadata(file);
            return {
                result: 'success', // Explicitly set result to 'success'
                file_metadata: {
                    ...baseValidation.file_metadata, // Contains the filename, type, size from base validation
                    ...jsonMetadata // Contains additional metadata extracted from JSON content
                }
            };
        } catch (error) {
            console.error("Error extracting JSON metadata:", error);
            return { result: 'fail', reason: 'Error processing JSON file' };
        }
    }
}
export default UserStoryFileUploadValidator