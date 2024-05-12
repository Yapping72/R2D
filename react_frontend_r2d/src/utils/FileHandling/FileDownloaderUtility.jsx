/**
 * FileDownloadUtility class
 * Provides methods to download various file types including JSON, TXT, and Markdown.
 * Supported file types: json, .txt, .md
 */

class FileDownloadUtility {
  /**
   * Downloads JSON content as a .json file.
   * If the content is a string, it will be parsed and then stringified for pretty printing.
   * If the content is an object, it will be directly stringified.
   * The downloaded file's name will be appended with a timestamp.
   * 
   * @param {string|object} fileContent - The content to download.
   * @param {string} fileName - The base name of the file to download.
   */
  static downloadJson(fileContent, fileName) {
    // Check if fileContent is a string and needs parsing, otherwise directly stringify
    const jsonString = typeof fileContent === "string" 
      ? JSON.stringify(JSON.parse(fileContent), null, 2) // Parse then stringify for pretty print
      : JSON.stringify(fileContent, null, 2); // Directly stringify the object

    const blob = new Blob([jsonString], { type: 'application/json' });
    this.download(blob, fileName);
  }
   /**
   * Downloads text content as a .txt file.
   * The downloaded file's name will be appended with a timestamp.
   * 
   * @param {string} fileContent - The content to download.
   * @param {string} fileName - The base name of the file to download.
   */
  static downloadTxt(fileContent, fileName) {
    const blob = new Blob([fileContent], { type: 'text/plain' });
    this.download(blob, fileName);
  }
    /**
   * Downloads Markdown content as a .md file.
   * The downloaded file's name will be appended with a timestamp.
   * 
   * @param {string} fileContent - The content to download.
   * @param {string} fileName - The base name of the file to download.
   */
  static downloadMd(fileContent, fileName) {
    const blob = new Blob([fileContent], { type: 'text/markdown' });
    this.download(blob, fileName);
  }
   /**
   * Helper method to handle the actual download process.
   * Creates a URL from the blob and triggers a download via a temporary HTML anchor element.
   * 
   * @param {Blob} blob - The blob of the content to download.
   * @param {string} fileName - The intended name of the file.
   */
  static download(blob, fileName) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = this.addTimestampToFileName(fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
 /**
   * Appends a timestamp to the filename to ensure uniqueness.
   * The timestamp is formatted as YYYY-MM-DDTHH-MM-SS.
   * 
   * @param {string} filename - The original filename without a timestamp.
   * @return {string} - The new filename appended with a timestamp.
   */
  static addTimestampToFileName(filename) {
    const baseName = filename.split('.').slice(0, -1).join('.');
    const extension = filename.split('.').pop();
    const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');
    return `${baseName}-${timestamp}.${extension}`;
  }
}

export default FileDownloadUtility