
MERMAID_SEQUENCE_DIAGRAM_SCHEMA = {
    "title": "SequenceDiagramResponse",
    "description": "Response containing sequence diagrams grouped by features.",
    "type": "object",
    "properties": {
        "diagrams": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "feature": {
                        "type": "array",
                        "description": "The feature that the sequence diagram is generated for",
                        "items": {
                            "type": "string"
                        }
                    },
                    "diagram": {
                        "type": "string",
                        "description": "The sequence diagram in Mermaid syntax containing primary flows, alternative flows, loops, actors, and messages"
                    },
                    "description": {
                        "type": "string",
                        "description": "The detailed description of primary flows, alternative flows, loops, actors, and messages in the diagram."
                    },
                    "actors": {
                        "type": "array",
                        "description": "The actors in the diagram",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "feature",
                    "diagram",
                    "description",
                    "actors"
                ]
            }
        }
    },
    "required": [
        "diagrams"
    ]
}
