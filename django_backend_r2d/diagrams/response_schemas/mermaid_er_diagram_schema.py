# A response schema is a dictionary that defines the structure of the response that is expected from the model.

# Response schema for the ERDiagramService
MERMAID_ER_DIAGRAM_SCHEMA = {
    "title": "ERDiagramResponse",
    "description": "Response containing ER diagrams grouped by features.",
    "type": "object",
    "properties": {
        "diagrams": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "feature": {
                        "type": "array",
                        "description": "The feature that the ER diagram is generated for",
                        "items": {
                            "type": "string"
                        }
                    },
                    "diagram": {
                        "type": "string",
                        "description": "The ER diagram in Mermaid syntax"
                    },
                    "description": {
                        "type": "string",
                        "description": "The detailed description of the classes, relationships, and attributes in the diagram"
                    },
                    "entities": {
                        "type": "array",
                        "description": "The entities in the diagram",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "feature",
                    "diagram",
                    "description",
                    "entities"
                ]
            }
        }
    },
    "required": [
        "diagrams"
    ]
}
