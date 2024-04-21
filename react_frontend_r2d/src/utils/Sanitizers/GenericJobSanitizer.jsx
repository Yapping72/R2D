/**
 * Abstract job sanitization class that mandates the getSanitizedData function.
 */
class GenericJobSanitizer {
    getSanitizedData(data) {
        throw new Error("Method 'getSanitizedData' must be implemented by subclass");
    }
}

export default GenericJobSanitizer;