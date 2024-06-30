# response_schemas.py

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
                },
                "required": ["feature", "diagram"],
            },
        },
    },
    "required": ["diagrams"],
}
