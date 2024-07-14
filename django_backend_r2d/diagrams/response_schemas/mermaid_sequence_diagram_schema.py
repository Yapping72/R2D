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
                        "type": "string",
                        "description": "The feature that the sequence diagram is generated for"
                    },
                    "diagram": {
                        "type": "string",
                        "description": "The sequence diagram in Mermaid syntax"
                    },
                    "description": {
                        "type": "string",
                        "description": "The description of the interactions and messages in the diagram"
                    },
                    "actors": {
                        "type": "array",
                        "description": "The actors in the diagram",
                        "items": {
                            "type": "string"
                        }
                    },
                    "messages": {
                        "type": "array",
                        "description": "The messages exchanged in the diagram",
                        "items": {
                            "type": "object",
                            "properties": {
                                "from": {
                                    "type": "string",
                                    "description": "The actor or object that sends the message"
                                },
                                "to": {
                                    "type": "string",
                                    "description": "The actor or object that receives the message"
                                },
                                "message": {
                                    "type": "string",
                                    "description": "The content of the message"
                                },
                                "type": {
                                    "type": "string",
                                    "description": "The type of interaction (e.g., message, response, create, delete)"
                                }
                            },
                            "required": [
                                "from",
                                "to",
                                "message"
                            ]
                        }
                    },
                    "alt_flows": {
                        "type": "array",
                        "description": "The alternative flows in the sequence diagram",
                        "items": {
                            "type": "object",
                            "properties": {
                                "condition": {
                                    "type": "string",
                                    "description": "The condition for the alternative flow"
                                },
                                "messages": {
                                    "type": "array",
                                    "description": "The messages in the alternative flow",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "from": {
                                                "type": "string",
                                                "description": "The actor or object that sends the message"
                                            },
                                            "to": {
                                                "type": "string",
                                                "description": "The actor or object that receives the message"
                                            },
                                            "message": {
                                                "type": "string",
                                                "description": "The content of the message"
                                            },
                                            "type": {
                                                "type": "string",
                                                "description": "The type of interaction (e.g., message, response, create, delete)"
                                            }
                                        },
                                        "required": [
                                            "from",
                                            "to",
                                            "message"
                                        ]
                                    }
                                }
                            },
                            "required": [
                                "condition",
                                "messages"
                            ]
                        }
                    },
                    "loops": {
                        "type": "array",
                        "description": "The loops in the sequence diagram",
                        "items": {
                            "type": "object",
                            "properties": {
                                "condition": {
                                    "type": "string",
                                    "description": "The condition for the loop"
                                },
                                "messages": {
                                    "type": "array",
                                    "description": "The messages within the loop",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "from": {
                                                "type": "string",
                                                "description": "The actor or object that sends the message"
                                            },
                                            "to": {
                                                "type": "string",
                                                "description": "The actor or object that receives the message"
                                            },
                                            "message": {
                                                "type": "string",
                                                "description": "The content of the message"
                                            },
                                            "type": {
                                                "type": "string",
                                                "description": "The type of interaction (e.g., message, response, create, delete)"
                                            }
                                        },
                                        "required": [
                                            "from",
                                            "to",
                                            "message"
                                        ]
                                    }
                                }
                            },
                            "required": [
                                "condition",
                                "messages"
                            ]
                        }
                    }
                },
                "required": [
                    "feature",
                    "diagram",
                    "description",
                    "actors",
                    "messages"
                ]
            }
        }
    },
    "required": [
        "diagrams"
    ]
}