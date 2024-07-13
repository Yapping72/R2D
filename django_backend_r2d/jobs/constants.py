from enum import Enum

class ValidJobStatus(Enum):
    """
    List of valid job status stored in JobStatus Table
    
    Enum Key               | id | name   | code 
    DRAFT                  | 1  | Draft  | 1 
    QUEUED                 | 2  | Queued | 2 
    SUBMITTED              | 3  | Submitted | 3 
    ERROR_FAILED_TO_SUBMIT | 4  | Error Failed to Submit | 4
    PROCESSING             | 5  | Processing | 5
    ERROR_FAILED_TO_PROCESS| 6  | Error Failed to Process | 6
    JOB_ABORTED            | 7  | Job Aborted | 7
    COMPLETED              | 8  | Completed | 8
    """
    DRAFT = "Draft"
    QUEUED = "Queued"
    SUBMITTED = "Submitted"
    ERROR_FAILED_TO_SUBMIT = "Error Failed to Submit"
    PROCESSING = "Processing"
    ERROR_FAILED_TO_PROCESS = "Error Failed to Process"
    JOB_ABORTED = "Job Aborted"
    COMPLETED = "Completed"

class ValidJobTypes(Enum):
    """
    List of valid job types allowed.
    
    Enum Key         | Value
    USER_STORY       | user_story
    CLASS_DIAGRAM    | class_diagram
    ER_DIAGRAM       | er_diagram
    SEQUENCE_DIAGRAM | sequence_diagram
    STATE_DIAGRAM    | state_diagram
    """
    USER_STORY = "user_story"
    CLASS_DIAGRAM = "class_diagram"
    ER_DIAGRAM = "er_diagram"
    SEQUENCE_DIAGRAM = "sequence_diagram"
    STATE_DIAGRAM = "state_diagram"

