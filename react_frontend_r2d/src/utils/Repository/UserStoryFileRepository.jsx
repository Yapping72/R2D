import {GenericIndexedDBRepository} from './GenericIndexedDBRepository'
import FileReaderUtility from '../FileHandling/FileReaderUtility';
import UserStoryFileUploadValidator from '../Validators/UserStoryFileUploadValidator';

/*
* Repository to retrieve and write requirements (JSON based)
*/

export class UserStoryFileRepository extends GenericIndexedDBRepository {
    constructor() {
      super("r2d-user-story-db", "user-story-file-store");
    }
    
    // Retrieves data stored in IndexedDB by id
    async handleFindById(id) {
        try{
            const result = await this.findById(id)
            // console.log("File and Metadata retrieved:", result);
            return { success: true, data: result};
        } catch(error) {
            console.error("Error retrieving user story file from DB: ", error);
            return { success: false, error: error.message };
        }
    }
    // Retrieves all requirements file uploaded
    async handleReadAllFiles() {
        try{
            const result = await this.readAllFiles();
            // console.log("All files retrieved", result);
            return { success: true, data: result};
        } catch(error) {
            console.error("Error retrieving all user story files from DB: ", error);
            return { success: false, error: error.message };
        }
    }
    // Writes the actual file and fileMeta to IndexedDb
    async handleWriteFileAndMetadataToDB(file, metadata) {
        try {
            const result = await this.writeFileAndMetadataToDB(file, metadata);
            return { success: true, data: result };
        } catch (error) {
            console.error("Error writing to user story file and metadata to DB:", error);
            return { success: false, error: error.message };
        }
    }
    // Deletes all records from DB
    async handleClearDb(){
        try { 
            const result = await this.clearDB()
            return { success: true };
        } catch(error) {
            console.error("Failed to clear IndexedDb file store: ", error)
            return { success: false, error: error.message };
        }
    }
    
    // Takes in an updated file and updates the record in db
    async commitRecordToDb(id, updatedFile) {
        const validator = new UserStoryFileUploadValidator();
        try {
            const validationResult = await validator.validate(updatedFile);
            if (validationResult.result === 'success') { 
                // Success: Store the file into db, append the generated id to fileMetadata
                const result = await this.updateFileAndMetadataToDB(id, updatedFile, validationResult.file_metadata)
                console.log(`Your file ${validationResult.file_metadata.filename} has been uploaded successfully.`)
                return { success: true, data: result };
            } else {
                console.error(`Your file could not be updated. Please check that the file meets uploading requirements.`)
                return { success: false, error: "File validation failed"};
            }
        }
        catch(error) {
            console.error("Failed to commit changes to IndexedDB. Commits will be reverted.")
            return { success: false, error: error.message };
        }   
    }

    // This method updates a specific record within a file
    // Reads the existing file contents
    // Updates the record to update based on record id
    // Rewrites the file back to db. 
    async updateRecordInFile(fileId, recordId, editedData) {
        try {
            const fileResponse = await this.findById(fileId);
            if (!fileResponse) {
                throw new Error('File not found.');
            }
            
            // Parse the file content and find the record to update
            const fileContent = await FileReaderUtility.readAsText(fileResponse.content); 
            const jsonContent = JSON.parse(fileContent);
            let recordUpdated = false;
            
            const updatedJsonContent = jsonContent.map(record => {
                if (record.record_identifier === recordId) {
                    recordUpdated = true;
                    return { ...record, ...editedData };
                }
                return record;
            });

            // If the record with the provided identifier was not found, throw an error
            if (!recordUpdated) {
                throw new Error('Record to update not found.');
            }

            // Convert the updated JSON content back into a Blob
            const updatedBlob = new Blob([JSON.stringify(updatedJsonContent, null, 2)], {
                type: 'application/json'
            });


            // Convert the Blob into a File Object properly
            const updatedBlobAsFile = new File([updatedBlob], fileResponse.filename || "default-filename.json", {
                type: 'application/json', 
                lastModified: new Date().getTime() 
            });
            

            // Use handleUpdateFileById to write the updated file back to the database
            const updateResponse = await this.commitRecordToDb(fileId, updatedBlobAsFile); 

            if (!updateResponse.success) {
                throw new Error(updateResponse.error);
            }
            
            return { success: true, message: 'Record updated successfully.' };
        } 
        catch (error) {
            console.error('Error updating record in file:', error);
            return { success: false, error: error.message };
        }
    }

    async addRecordToFile(fileId, newData) {
        try {
            const fileResponse = await this.findById(fileId);
            if (!fileResponse) {
                throw new Error('File not found.');
            }
            
            // Retrieve file contents and add newData to the file
            const fileContent = await FileReaderUtility.readAsText(fileResponse.content); 
            const jsonContent = JSON.parse(fileContent);
            jsonContent.push(newData)

            // Convert the JSON content back into a Blob
            const updatedBlob = new Blob([JSON.stringify(jsonContent, null, 2)], {
                type: 'application/json'
            });


            // Convert the Blob into a File Object properly
            const updatedBlobAsFile = new File([updatedBlob], fileResponse.filename || "default-filename.json", {
                type: 'application/json', 
                lastModified: new Date().getTime() 
            });
            

            // Use handleUpdateFileById to write the updated file back to the database
            const updateResponse = await this.commitRecordToDb(fileId, updatedBlobAsFile); 
            if (!updateResponse.success) {
                throw new Error(updateResponse.error);
            }
            
            return { success: true, message: 'Record updated successfully.' };
        } 
        catch (error) {
            console.error('Error updating record in file:', error);
            return { success: false, error: error.message };
        }
    }
}
  