import RequirementsCardGrid from '../Cards/RequirementsCardGrid'
import {Container} from '@mui/material'

/**
 * `FeatureVisualizer` renders an expandable accordion for a given file.
 * Inside each accordion, there is a `RequirementsCardGrid` which displays
 * all the requirements or user stories (US) associated with that file's feature.
 * 
 * Props:
 * - `title` (string): The title for the accordion
 *    associated with the feature. This is used to fetch data or as part of the data retrieval logic.
 * - `featureData` (Array): The data for the feature, which will be displayed in the RequirementsCardGrid. It defaults to an empty array.
 * 
 * @param {Object} props - The props object for the component.
 * @param {string} [props.fileName] - The name of the file to reference for requirement data, defaulting to "test.json".
 * @param {Array} [props.featureData] - The array of data for the feature requirements, defaulting to an empty array.
 * @returns {ReactElement} The `FeatureVisualizer` component with a `R2DAccordion` and `RequirementsCardGrid`.
 */

const FeatureVisualizer = ({title = "Upload Requirements to Begin", featureData=[], fileId})=> {
    
    return (
        <Container>  
        <RequirementsCardGrid featureData={featureData} fileId={fileId}></RequirementsCardGrid>
        </Container>
    )
}

export default FeatureVisualizer