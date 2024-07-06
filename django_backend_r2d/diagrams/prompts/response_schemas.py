# Define new response schemas here. 
# A response schema is a dictionary that defines the structure of the response that is expected from the model.

# Response schema for the ClassDiagramService
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
                        "type": "array",
                        "description": "The feature that the class diagram is generated for",
                        "items": {
                            "type": "string"
                        }
                    },
                    "diagram": {
                        "type": "string",
                        "description": "The class diagram in Mermaid syntax"
                    },
                    "description": {
                        "type": "string",
                        "description": "The description of the classes, relationships, and attributes in the diagram"
                    },
                    "classes": {
                        "type": "array",
                        "description": "The classes in the diagram",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "feature",
                    "diagram",
                    "description",
                    "classes"
                ]
            }
        }
    },
    "required": [
        "diagrams"
    ]
}