/**
 * FileUploadValidator class.
 * This generic utility class provides static methods for validating files based on their extensions,
 * size, and line count. By default it supports .json, .mermaid, and .txt files, enforces a maximum file size of 15 MB,
 * and restricts files to a maximum of 1000 lines. Validation results are returned in a structured format,
 * indicating success or failure along with relevant metadata or error messages.
 * Inheriting classes can augment the validate function by invoking the base functions here and any other validation it requires
 */

class FileUploadValidator {
    constructor(validExtensions = ['json', 'mermaid', 'txt'], maxFileSize = 15 * 1024 * 1024, maxLineCount = 1000) {
        this.validExtensions = validExtensions;
        this.maxFileSize = maxFileSize;
        this.maxLineCount = maxLineCount;
    }

    getValidExtensions() {
        return this.validExtensions.map(ext => `.${ext}`).join(", ");
    }

    getMaxFileSize() {
        return this.maxFileSize;
    }

    getMaxLineCount() {
        return this.maxLineCount;
    }
    
    /**
     * Extracts and returns metadata from a file.
     * @param {File} file - The file from which to extract metadata.
     * @returns An object containing initial metadata (lines set to null, size, filename, and file type).
     */
    getFileMetadata(file) {
        return {
            "filename": file.name,
            "type": file.type,
            "size": `${file.size} bytes`,
            "lines": null,
        };
    }

    /**
     * Validates the file extension.
     * @param {File} file - The file to validate.
     * @returns {boolean} - True if the file extension is valid, false otherwise.
    */
    validateFileExtension(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        console.log(extension)
        console.log(this.validExtensions)
        return this.validExtensions.includes(extension);
    }

    /**
     * Validates the file size.
     * @param {File} file - The file to validate.
     * @returns {boolean} - True if the file size is within the limit, false otherwise.
    */
    validateFileSize(file) {
        return file.size <= this.maxFileSize;
    }

    /**
     * Validates the number of lines in the file.
     * @param {File} file - The file to validate.
     * @returns {Promise<boolean|number>} - A promise that resolves with the number of lines if under the limit, or false otherwise.
     */
    async validateLineCount(file) {
        const reader = new FileReader();
        
        return new Promise((resolve) => {
            reader.onload = (e) => {
                const text = e.target.result;
                const lines = text.split(/\r\n|\n/);
                resolve(lines.length <= this.maxLineCount ? lines.length : false);
            };
            reader.onerror = () => resolve(false);
            reader.readAsText(file);
        });
    }

    /**
     * Validates the file based on extension, size, and line count.
     * @param {File} file - The file to validate.
     * @returns {Promise<Object>} - A promise that resolves with an object indicating validation success or failure, along with relevant data.
     */
    async validate(file) {
        console.log("File to validate:", file);
        if (!file) {
            console.error("No file provided for validation");
            return { result: 'fail', message: `An error occurred during file validation: No file was provided}` };
        }

        try {
            if (!this.validateFileExtension(file)) {
                console.error("File validation failed: Invalid file extension");
                return { result: 'fail', message: 'Invalid file extension' };
            }

            if (!this.validateFileSize(file)) {
                console.error("File validation failed: File size exceeds limit");
                return { result: 'fail', message: 'File size exceeds limit' };
            }

            const lineCount = await this.validateLineCount(file);
            if (lineCount === false) {
                console.error("File validation failed: File has too many lines");
                return { result: 'fail', message: 'File has too many lines' };
            }

            const fileMetadata = this.getFileMetadata(file);
            fileMetadata.lines = lineCount; 
            return { result: 'success', file_metadata: fileMetadata };
        }
        catch (error) {
            console.error('Error validating file:', error);
            // Return a structured error message to indicate a failure in the validation process
            return { result: 'fail', message: `An error occurred during file validation: ${error.message}` };
        }
    }
}

export default FileUploadValidator;
