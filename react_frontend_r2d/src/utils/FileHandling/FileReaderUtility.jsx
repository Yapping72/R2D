class FileReaderUtility {
    /**
     * Reads the content of a file as text.
     * @param {File} file The file to read.
     * @returns {Promise<string>} A promise that resolves with the text content of the file.
     */
    static readAsText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error);
        reader.readAsText(file);
      });
    }
  
    /**
     * Reads the content of a file as an ArrayBuffer (useful for binary files).
     * @param {File} file The file to read.
     * @returns {Promise<ArrayBuffer>} A promise that resolves with the ArrayBuffer of the file.
     */
    static readAsArrayBuffer(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error);
        reader.readAsArrayBuffer(file);
      });
    }
  
    /**
     * Reads the content of a file as a Data URL (useful for images and other media).
     * @param {File} file The file to read.
     * @returns {Promise<string>} A promise that resolves with the Data URL of the file.
     */
    static readAsDataURL(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error);
        reader.readAsDataURL(file);
      });
    }
  }
  
  export default FileReaderUtility;
  