import React from 'react';
import JobAccordion from '../Accordion/JobAccordion';
import UserStoryJobCardGrid from '../Cards/UserStoryJobCardGrid';
import InformationPaperCard from '../Cards/InformationPaperCard';


const UserStoryJobParametersVisualizer = ({ jobParameters }) => {
    // Check if jobParameters is null or undefined and render a placeholder if so
    if (!jobParameters) {
        return (
            <InformationPaperCard title="Job parameter guidelines" description="Placeholder Content">
            </InformationPaperCard>
        );
    }

    // Render the JobAccordion with the UserStoryJobCardGrid as a child if jobParameters exist
    return (
        <JobAccordion jobParameters={jobParameters}>
            <UserStoryJobCardGrid jobParameters={jobParameters} />
        </JobAccordion>
    );
}

export default UserStoryJobParametersVisualizer;