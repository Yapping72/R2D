import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DragDropFile from "../FileUpload/DragDropFileUpload";
import UserStoryFileUploadValidator from '../../../utils/Validators/UserStoryFileUploadValidator';
import { UserStoryFileRepository } from "../../../utils/Repository/UserStoryFileRepository";
import R2DModal from '../Modals/R2DModal';
import { useUserStoryContext } from './UserStoryContextProvider';
import FileReaderUtility from '../../../utils/FileHandling/FileReaderUtility';
import ClearIndexedDbButton from '../../ui/Button/ClearIndexedDbButton';
import { v4 as uuidv4 } from 'uuid';


const UserStoryManagementModal = () => {
    const { _, handleFileUpload } = useUserStoryContext();
    /*
    * Adds a record identifier to each requirement record
    */
    const handleFilePreProcessing = async (file) => {
        try {
            const fileContents = await FileReaderUtility.readAsText(file);
            const jsonFileContents = JSON.parse(fileContents);

            // Modify each item in the array to include a "record_identifier" UUID
            const modifiedJsonContents = jsonFileContents.map(item => ({
                ...item,
                record_identifier: uuidv4(), // Add a unique UUID
            }));

            // Convert the modified JSON back into a Blob object
            const modifiedFileBlob = new Blob(
                [JSON.stringify(modifiedJsonContents, null, 2)], // Add indentation for readability
                { type: 'application/json' });
            return modifiedFileBlob; // Return the new Blob for further use
        } catch (error) {
            console.error("Error during file pre-processing:", error);
            throw error;
        }
    };

    return (
        <R2DModal title="Upload User Stories" icon={<CloudUploadIcon></CloudUploadIcon>}>
            <DragDropFile
                validator={new UserStoryFileUploadValidator(['json'])}
                repository={new UserStoryFileRepository()}
                IconComponent={CloudUploadIcon}
                handleFileUpload={handleFileUpload}
                handleFilePreProcessing={handleFilePreProcessing}>
            </DragDropFile>
            <ClearIndexedDbButton repository={new UserStoryFileRepository()}></ClearIndexedDbButton>
        </R2DModal>
    );
}

export default UserStoryManagementModal