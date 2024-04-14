import FileReaderUtility from '../../utils/FileReaders/FileReaderUtility';
import { RequirementsFileRepository } from '../../utils/Repository/RequirementsFileRepository';


const RequirementsManager = () => {

    const saveRequirementEdits = async (fileId, recordId, editedData) => {
        try {
            const repository = new RequirementsFileRepository();
            const response = await repository.handleFindById(fileId);
           
            if (response.success && response.data) {
                // Assuming the file content is JSON and contains an array of records
                const fileContents = await FileReaderUtility.readAsText(response.data.content);  
                const jsonFileContents= JSON.parse(fileContents);
                for (let i=0; i< jsonFileContents.length; i++) {
                    if (jsonFileContents[i].recordId == recordId) {
                        console.log(jsonFileContents[i]);
                        // Update contents here
                    }
                }
            }
            
    } catch (error) {
            console.error("Error encountered while trying to save changes to requirements:", error);
        }
    };
}