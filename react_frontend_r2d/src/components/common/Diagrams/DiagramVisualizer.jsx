import React, { useEffect, useState, useRef } from 'react';
import { Backdrop, Box, Card, CardContent, Paper, Typography, Divider, TextField, Button,Chip } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import MermaidRenderer from '../Mermaid/MermaidRenderer';
import './diagramVisualizer.css';
import ZoomAndPan from '../../ui/Interactions/ZoomAndPan';
import ApiManager from '../../../utils/Api/ApiManager';
import UrlsConfig from '../../../utils/Api/UrlsConfig';
import FileDownloadUtility from '../../../utils/FileHandling/FileDownloaderUtility';

/*
const response = 
{
  "data": {
    "job_id": "6153c46e-1453-41cc-ab3a-03fb5af35841",
    "diagrams": {
      "class_diagrams": [
        {
          "id": 731,
          "job_id": "6153c46e-1453-41cc-ab3a-03fb5af35841",
          "model_id": 2,
          "feature": [
            "Authentication Authorization & Session Management"
          ],
          "diagram": "classDiagram\n    class User {\n        +String email\n        +String password\n        +login()\n        +register()\n    }\n    class AuthenticationController {\n        +login(User user)\n        +register(User user)\n    }\n    class IUserAuthentication {\n        +login()\n        +register()\n    }\n    User ..|> IUserAuthentication : Implements\n    AuthenticationController --> User : Uses\n\n    class JWT {\n        +String token\n        +validateToken()\n        +generateToken()\n    }\n    class AuthorizationController {\n        +authorize(JWT jwt)\n    }\n    class IAuthorization {\n        +authorize()\n    }\n    JWT ..|> IAuthorization : Implements\n    AuthorizationController --> JWT : Uses\n\n    class Session {\n        +String sessionId\n        +Boolean isActive\n        +terminateSession()\n    }\n    class SessionController {\n        +manageSession(Session session)\n    }\n    class ISessionManagement {\n        +manageSession()\n    }\n    Session ..|> ISessionManagement : Implements\n    SessionController --> Session : Uses\n\n    class CloudWatch {\n        +logEvent()\n    }\n    class SIT_CAPSTONE_YP {\n        +monitor()\n    }\n    CloudWatch --> SIT_CAPSTONE_YP : Monitors",
          "description": "This diagram covers the Authentication, Authorization, and Session Management features. \n- The **User** class represents the entity that can login and register. Methods include login and register, which handle user authentication. \n- **AuthenticationController** uses the User class to process login and registration requests. \n- **IUserAuthentication** is an interface that ensures the User class adheres to the authentication methods. \n- **JWT** handles token generation and validation, crucial for authorization. \n- **AuthorizationController** uses JWT to authorize user actions. \n- **IAuthorization** is an interface that ensures JWT implements authorization methods. \n- **Session** represents user sessions, with methods to terminate them. \n- **SessionController** manages user sessions. \n- **ISessionManagement** is an interface for session management methods. \n- **CloudWatch** logs events, and **SIT_CAPSTONE_YP** monitors these logs as per AWS recommendation.",
          "classes": [
            "User",
            "AuthenticationController",
            "JWT",
            "AuthorizationController",
            "Session",
            "SessionController",
            "CloudWatch",
            "SIT_CAPSTONE_YP"
          ],
          "helper_classes": [
            "IUserAuthentication",
            "IAuthorization",
            "ISessionManagement"
          ],
          "is_audited": true,
          "created_timestamp": "2024-11-12T15:16:13.422133Z",
          "last_updated_timestamp": "2024-11-12T15:16:13.422146Z"
        }
      ],
      "er_diagrams": [
        {
          "id": 526,
          "job_id": "d411b316-ef11-4e85-a0d2-88d30f165e0d",
          "model_id": 2,
          "feature": [
            "Authentication",
            "Authorization",
            "Session Management"
          ],
          "diagram": "erDiagram\n    User {\n        int userID PK\n        string username\n        string password\n        string email\n    }\n    AuthenticationController ||--o{ User : \"manages\"\n    IUserAuthentication ||--o{ User : \"defines methods for\"\n    JWT {\n        int jwtID PK\n        string token\n    }\n    AuthorizationController ||--o{ JWT : \"uses\"\n    IAuthorization ||--o{ JWT : \"ensures implementation of\"\n    Session {\n        int sessionID PK\n        int userID FK\n        datetime startTime\n        datetime endTime\n    }\n    SessionController ||--o{ Session : \"manages\"\n    ISessionManagement ||--o{ Session : \"defines methods for\"\n    CloudWatch {\n        int logID PK\n        string logDetails\n    }\n    SIT_CAPSTONE_YP ||--o{ CloudWatch : \"monitors\"",
          "description": "This diagram covers the Authentication, Authorization, and Session Management features:\n- The **User** entity represents individuals who can login and register. Attributes include userID (PK), username, password, and email.\n- **AuthenticationController** manages user authentication processes.\n- **IUserAuthentication** is an interface that defines the authentication methods for the User entity.\n- **JWT** handles token generation and validation, crucial for authorization. Attributes include jwtID (PK) and token.\n- **AuthorizationController** uses JWT to authorize user actions.\n- **IAuthorization** is an interface that ensures JWT implements authorization methods.\n- **Session** represents user sessions, linked to users via userID (FK). Attributes include sessionID (PK), startTime, and endTime.\n- **SessionController** manages user sessions.\n- **ISessionManagement** is an interface for session management methods.\n- **CloudWatch** logs events, and **SIT_CAPT...  Read More",
          "entities": [
            "User",
            "AuthenticationController",
            "IUserAuthentication",
            "JWT",
            "AuthorizationController",
            "IAuthorization",
            "Session",
            "SessionController",
            "ISessionManagement",
            "CloudWatch",
            "SIT_CAPSTONE_YP"
          ],
          "is_audited": true,
          "created_timestamp": "2024-11-12T15:16:48.002783Z",
          "last_updated_timestamp": "2024-11-12T15:16:48.002803Z"
        }
      ],
      "sequence_diagrams": [
        {
          "id": 94,
          "job_id": "e71af6a1-7685-40d6-9819-8f107d3041be",
          "model_id": 2,
          "feature": [
            "Authentication",
            "Authorization",
            "Session Management"
          ],
          "diagram": "sequenceDiagram\n    actor User\n    participant AuthenticationController as AuthCtrl\n    participant IUserAuthentication as IUserAuth\n    participant JWT\n    participant AuthorizationController as AuthzCtrl\n    participant IAuthorization as IAuthz\n    participant SessionController as SessionCtrl\n    participant ISessionManagement as ISessionMgmt\n    participant CloudWatch\n    participant Database\n\n    User ->> AuthCtrl: Request login (SIT email & password)\n    AuthCtrl ->> IUserAuth: Validate credentials\n    alt Valid credentials\n        IUserAuth -->> AuthCtrl: Credentials valid\n        AuthCtrl ->> JWT: Create token\n        JWT -->> AuthCtrl: Token created\n        AuthCtrl ->> User: Login successful (JWT token)\n    else Invalid credentials\n        IUserAuth -->> AuthCtrl: Credentials invalid\n        AuthCtrl -->> User: Login failed\n    end\n\n    User ->> AuthzCtrl: Request access (JWT token)\n    AuthzCtrl ->> IAuthz: Verify token\n    alt Token valid\n        IAuthz -->> AuthzCtrl: Token verified\n        AuthzCtrl -->> User: Access granted\n    else Token invalid\n        IAuthz -->> AuthzCtrl: Token verification failed\n        AuthzCtrl -->> User: Access denied\n    end\n\n    User ->> SessionCtrl: Start session\n    SessionCtrl ->> ISessionMgmt: Create session\n    ISessionMgmt -->> Database: Save session\n    Database -->> ISessionMgmt: Session saved\n    ISessionMgmt -->> SessionCtrl: Session started\n    SessionCtrl -->> User: Session details\n\n    loop Every Event\n        User ->> CloudWatch: Log event\n    end",
          "description": "This sequence diagram represents the interactions among various components for Authentication, Authorization, and Session Management features. Primary flows include user login, token generation, access verification, session management, and event logging. Alternative flows handle scenarios such as invalid credentials and token verification failures. A loop demonstrates continuous event logging.",
          "actors": [
            "User",
            "AuthenticationController",
            "IUserAuthentication",
            "JWT",
            "AuthorizationController",
            "IAuthorization",
            "SessionController",
            "ISessionManagement",
            "CloudWatch",
            "Database"
          ],
          "is_audited": true,
          "created_timestamp": "2024-11-12T15:17:21.931964Z",
          "last_updated_timestamp": "2024-11-12T15:17:21.931982Z"
        }
      ]
    }
  },
  "message": "Retrieved diagrams for 6153c46e-1453-41cc-ab3a-03fb5af35841 successfully.",
  "success": true,
  "status_code": 200
}
*/

const DiagramVisualizer = ({ jobId, open, onClose }) => {
    const [selectedDiagrams, setSelectedDiagrams] = useState({});
    const [visualizeDiagram, setVisualizeDiagram] = useState(false);
    const scrollToBottomRef = useRef(null);

    useEffect(() => {
        if (open) {
            fetchDiagrams();
        }
    }, [open]);

    const fetchDiagrams = async () => {
        // API Call to fetch diagrams based on the job ID
        try {
            const result = await ApiManager.postData(UrlsConfig.endpoints.GET_ALL_DIAGRAMS, { job_id: jobId });
            if (result.success) {
                setSelectedDiagrams(result.data.diagrams);
            } 
        } catch (error) {
            // Handle unexpected errors
            console.error('Job Processing Error:', error);
        }
    };


    const handleRenderDiagram = (visualizeDiagram) => { 
        setVisualizeDiagram(visualizeDiagram);
          // Scroll to the bottom after rendering the diagram
          if (scrollToBottomRef.current) {
            scrollToBottomRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    };

    const cleanDescription = (text) => {
        return text.replace(/[*-]+/g, '').trim(); // Removes `**`, `*`, and `-` characters
    };


    const getCurrentTimestamp = () => {
        return new Date().toISOString().replace(/:/g, '-').split('.')[0];
    };

    const handleDownloadDiagram = (diagram, diagramType) => {
        const fileName = `${diagramType}_${getCurrentTimestamp()}.txt`;
        FileDownloadUtility.downloadTxt(diagram, fileName);
    };

    return (
        <Backdrop open={open} sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            {/* Prevent backdrop click from closing the modal by stopping event propagation */}
            <Paper 
                elevation={3} 
                onClick={(e) => e.stopPropagation()} // Stop event propagation here
                sx={{ p: 3, backgroundColor: '#2c2c2c', color: '#ffffff', width: '95%', maxHeight: '80%', overflow: 'auto' }}
            >
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h5" fontWeight="bold" color="primary">
                        Diagram Details for Job ID: {jobId}
                    </Typography>
                    <Button onClick={onClose} startIcon={<CloseIcon />} color="inherit">Close</Button>
                </Box>
                
                {/* Iterate over each diagram type */}
                {Object.keys(selectedDiagrams).map((diagramType) =>
                    selectedDiagrams[diagramType]?.map((diagram, index) => (
                        <Card key={`${diagramType}-${index}`} variant="outlined" sx={{ mb: 2, backgroundColor: '#424242' }}>
                            <CardContent>
                                {/* Diagram Type Title */}
                                <Typography variant="h6" color="secondary" gutterBottom>
                                    {diagramType.replace(/_/g, ' ').toUpperCase()}
                                </Typography>

                                {/* Cleaned Description Section */}
                                {diagram.description && (
                                    <Typography variant="body2" sx={{ mb: 2, color: '#d3d3d3' }}>
                                        {cleanDescription(diagram.description)}
                                    </Typography>
                                )}

                                <Divider sx={{ my: 2 }} />

                                {/* Attributes Section */}
                                <Box display="flex" flexWrap="wrap" gap={2}>
                                    {diagram.classes && (
                                        <Box>
                                            <Typography variant="subtitle2">Classes:</Typography>
                                            <ul style={{ margin: 0, paddingLeft: '1.25em' }}>
                                                {diagram.classes.map((item, idx) => (
                                                    <li key={idx}>
                                                        <Typography variant="body2" component="span">{item}</Typography>
                                                    </li>
                                                ))}
                                            </ul>
                                        </Box>
                                    )}
                                    {diagram.entities && (
                                        <Box>
                                            <Typography variant="subtitle2">Entities:</Typography>
                                            <ul style={{ margin: 0, paddingLeft: '1.25em' }}>
                                                {diagram.entities.map((item, idx) => (
                                                    <li key={idx}>
                                                        <Typography variant="body2" component="span">{item}</Typography>
                                                    </li>
                                                ))}
                                            </ul>
                                        </Box>
                                    )}
                                    {diagram.actors && (
                                        <Box>
                                            <Typography variant="subtitle2">Actors:</Typography>
                                            <ul style={{ margin: 0, paddingLeft: '1.25em' }}>
                                                {diagram.actors.map((item, idx) => (
                                                    <li key={idx}>
                                                        <Typography variant="body2" component="span">{item}</Typography>
                                                    </li>
                                                ))}
                                            </ul>
                                        </Box>
                                    )}
                                    {diagram.helper_classes && (
                                        <Box>
                                            <Typography variant="subtitle2">Helper Classes:</Typography>
                                            <ul style={{ margin: 0, paddingLeft: '1.25em' }}>
                                                {diagram.helper_classes.map((item, idx) => (
                                                    <li key={idx}>
                                                        <Typography variant="body2" component="span">{item}</Typography>
                                                    </li>
                                                ))}
                                            </ul>
                                        </Box>
                                    )}
                                    {diagram.created_timestamp && (
                                        <Box>
                                            <Typography variant="subtitle2">Created:</Typography>
                                            <Chip
                                                label={new Date(diagram.created_timestamp).toLocaleString()}
                                                variant="outlined"
                                                color="primary"
                                                size="small"
                                                sx={{ mt: 0.5 }}
                                            />
                                        </Box>
                                    )}
                                    {diagram.last_updated_timestamp && (
                                        <Box>
                                            <Typography variant="subtitle2">Last Updated:</Typography>
                                            <Chip
                                                label={new Date(diagram.last_updated_timestamp).toLocaleString()}
                                                variant="outlined"
                                                color="primary"
                                                size="small"
                                                sx={{ mt: 0.5 }}
                                            />
                                        </Box>
                                    )}
                                </Box>

                                <Divider sx={{ my: 2 }} />
                                {/* Mermaid Diagram Text Field */}
                                {diagram.diagram && (
                                    <TextField
                                        label="Mermaid Diagram Code"
                                        multiline
                                        rows={6}
                                        fullWidth
                                        value={diagram.diagram}
                                        variant="outlined"
                                        InputProps={{
                                            readOnly: false,
                                        }}
                                        sx={{ backgroundColor: '#2c2c2c', color: '#ffffff', mt: 2 }}
                                    />
                                )}
                                 {/* Render Diagram Button */}
                                 {diagram.diagram && (
                                    <Button
                                        variant="outlined"
                                        color="primary"
                                        onClick={() => handleRenderDiagram(diagram.diagram)}
                                        sx={{ mt: 2, mr: 2 }}
                                    >
                                        Render Diagram
                                    </Button>
                                )}

                                <Button
                                        variant="outlined"
                                        color="secondary"
                                        onClick={() => handleDownloadDiagram(diagram.diagram, diagramType)}
                                        sx={{ mt: 2 }}
                                        >
                                        Download
                                </Button>
                            </CardContent>
                        </Card>
                    ))
                )}

                {/* Diagram Renderer */}
                {/* Mermaid Renderer Component */}
                <div ref={scrollToBottomRef}>
                    {visualizeDiagram && (
                    <Box className='drawioGrid' sx={{ height: '100vh', width: '100%' }}>
                    <ZoomAndPan >
                        <MermaidRenderer chart={visualizeDiagram} />
                    </ZoomAndPan>
                    </Box>
                )}
                </div>
            </Paper>
        </Backdrop>
    );
};

export default DiagramVisualizer;