import MermaidTable from "../../components/common/Mermaid/MermaidTable"
import { AlertProvider } from '../../components/common/Alerts/AlertContext';

function UploadRequirementsPage(){
    return (
        <>
        <AlertProvider>
            <MermaidTable></MermaidTable>
        </AlertProvider>
        </>

    )
}

export default UploadRequirementsPage