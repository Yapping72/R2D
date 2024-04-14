/*
* FileDownload utility class
* Supported file types = json, .txt, .md
**/


class FileDownloadUtility {
    static downloadJson(fileContent, fileName) {
      const jsonString = JSON.stringify(JSON.parse(fileContent), null, 2);  // Pretty print with 2 spaces
      const blob = new Blob([jsonString], { type: 'application/json' });
      this.download(blob, fileName);
    }
  
    static downloadTxt(fileContent, fileName) {
      const blob = new Blob([fileContent], { type: 'text/plain' });
      this.download(blob, fileName);
    }
  
    static downloadMd(fileContent, fileName) {
      const blob = new Blob([fileContent], { type: 'text/markdown' });
      this.download(blob, fileName);
    }
  
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
    static addTimestampToFileName(filename) {
      const baseName = filename.split('.').slice(0, -1).join('.');
      const extension = filename.split('.').pop();
      const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');
      return `${baseName}-${timestamp}.${extension}`;
    }
}

export default FileDownloadUtility