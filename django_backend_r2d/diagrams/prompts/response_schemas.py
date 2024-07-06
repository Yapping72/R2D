# Define new response schemas here. 
# A response schema is a dictionary that defines the structure of the response that is expected from the model.

"""
Response Schema for the structured output of the class diagram service.
"""
MERMAID_CLASS_DIAGRAM_SCHEMA = {
    "title": "ClassDiagramResponse",
    "description": "Response containing class diagrams grouped by features.",
    "type": "object",
    "properties": {
        "diagrams": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "feature": {
                        "type": "string",
                        "description": "The feature name",
                    },
                    "diagram": {
                        "type": "string",
                        "description": "The class diagram in Mermaid syntax",
                    },
                    "description": {    
                        "type": "string",
                        "description": "The description of the classes, their relationships and which user stories they cover."    
                    }
                },
                "required": ["feature", "diagram"],
            },
        },
    },
    "required": ["diagrams"],
}
