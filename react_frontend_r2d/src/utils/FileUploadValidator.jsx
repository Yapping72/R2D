
class FileUploadValidator {
    static validExtensions = ['json', 'mermaid', 'txt'];
    static maxFileSize = 15 * 1024 * 1024; // 15 MB in bytes
    static maxLineCount = 1000;

    static getFileMetadata(file) {
        return {
            lines: null,
            size: file.size,
            filename: file.name,
            type: file.type
        };
    }

    static validateFileExtension(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        return this.validExtensions.includes(extension);
    }

    static validateFileSize(file) {
        return file.size <= this.maxFileSize;
    }

    static async validateLineCount(file) {
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

    static async validate(file) {
        if (!this.validateFileExtension(file)) {
            return { result: 'fail', message: 'Invalid file extension' };
        }

        if (!this.validateFileSize(file)) {
            return { result: 'fail', message: 'File size exceeds limit' };
        }

        const lineCount = await this.validateLineCount(file);
        if (lineCount === false) {
            return { result: 'fail', message: 'File has too many lines' };
        }

        const fileMetadata = this.getFileMetadata(file);
        fileMetadata.lines = lineCount; // Update line count in metadata

        return { result: 'success', file_metadata: fileMetadata };
    }
}

export default FileUploadValidator;
