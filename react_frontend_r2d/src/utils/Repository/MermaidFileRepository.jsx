import {GenericFileRepository} from './GenericFileRepository'

/*
* Wrapper class for GenericIndexedDBRepository
* Returns  
* filename: file.name,
            type: file.type,
            size: file.size,
            lines: null, }
*/
export class MermaidFileRepository extends GenericFileRepository {
    constructor() {
      super("r2d-file-db", "mermaid-file-store"); // Must match what is stored in GenericFileRepository
    }

    async handleFindById(id) {
        try{
            const result = await this.findById(id)
            // console.log("File and Metadata retrieved:", result);
            return { success: true, data: result};
        } catch(error) {
            console.error("Error retrieving mermaid file from DB: ", error);
            return { success: false, error: error.message };
        }
    }

    async handleReadAllFiles() {
        try{
            const result = await this.readAllFiles();
            // console.log("All files retrieved", result);
            return { success: true, data: result};
        } catch(error) {
            console.error("Error retrieving all mermaid files from DB: ", error);
            return { success: false, error: error.message };
        }
    }

    async handleWriteFileAndMetadataToDB(file, metadata) {
        try {
            const result = await this.writeFileAndMetadataToDB(file, metadata);
            return { success: true, data: result };
        } catch (error) {
            console.error("Error writing file and metadata to DB:", error);
            return { success: false, error: error.message };
        }
    }

    async handleClearDb(){
        try { 
            const result = await this.clearDB()
            return { success: true };
        } catch(error) {
            console.error("Failed to clear IndexedDb file store: ", error)
            return { success: false, error: error.message };
        }
    }
}
  