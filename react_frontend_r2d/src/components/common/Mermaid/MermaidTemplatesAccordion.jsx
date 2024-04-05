import React from "react";
import {Button, ButtonGroup} from "@mui/material";
import R2DAccordion from "../Accordion/R2DAccordion";
import LightbulbIcon from '@mui/icons-material/Lightbulb';

export const mermaidExamples = [
    {
      "name": "Flow Chart",
      "content": "graph TD;\nA[Request] --> B{Controller};\nB --> C[Model];\nC --> D[View];\nD --> E[Response];\nC --> F[Database];\nF --> C;"
    },
    {
      "name": "Sequence Diagram",
      "content": "sequenceDiagram\nparticipant U as User\nparticipant UI as User Interface\nparticipant C as Controller\nparticipant S as UserService\nparticipant R as UserRepository\n\nU->>+UI: Enters registration details\nUI->>+C: Submits registration\nC->>+S: Create user\nS->>+R: Save new user\nR-->>-S: User saved\nS-->>-C: User created\nC-->>-UI: Display success message\nUI-->>-U: Views confirmation"
    },
    {
      "name": "Class Diagram",
      "content": "classDiagram\nBlogController : +listPosts()\nBlogController : +viewPost(id)\nBlogController : +addPost(postData)\nBlogController : +deletePost(id)\nPostService : +getAllPosts()\nPostService : +getPostById(id)\nPostService : +createPost(postData)\nPostService : +removePost(id)\nPostRepository : +findAll()\nPostRepository : +findById(id)\nPostRepository : +save(post)\nPostRepository : +deleteById(id)\nPost : -int id\nPost : -String title\nPost : -String content\nPost : -Date createdAt\nBlogController --> PostService : uses\nPostService --> PostRepository : uses\nPostRepository ..> Post : manages"
    },
    {
        "name": "State Diagram",
        "content": "stateDiagram-v2\n    [*] --> Idle\n    Idle --> Processing: Event Triggered\n    Processing --> Idle: Task Complete\n    Idle --> Sleep: No Activity\n    Sleep --> Idle: Interrupt\n    Processing --> Sleep: Low Power Mode Enabled\n    Sleep --> Processing: Interrupt + High Priority Task"
      },
    {
      "name": "ER Diagram",
      "content": "erDiagram\nCUSTOMER ||--o{ ORDER : places\nORDER ||--|{ ORDER_LINE : includes\nORDER_LINE }|--|{ PRODUCT : \"ordered in\"\nPRODUCT }|--|| PRODUCT_CATEGORY : categorized under\nCUSTOMER {\nstring email PK\nstring name\nstring password\n}\nORDER {\nint id PK\ndate orderDate\nstring status\n}\nORDER_LINE {\nint id PK\nint quantity\n}\nPRODUCT {\nint id PK\nstring name\nfloat price\n}\nPRODUCT_CATEGORY {\nint id PK\nstring name\n}"
    },
    {
      "name": "Data Flow Diagram",
      "content": "graph TD;\nA[Client] -->|requests| B(Controller)\nB -->|uses| C(Service)\nC -->|accesses| D(Repository)\nD -->|CRUD operations| E(Database)\nD --> C\nC --> B\nB -->|response| A"
    }
  ];

  const MermaidTemplatesAccordion = ({ onExampleSelect }) => {
    const handleExampleSelect = (content) => {
      if (onExampleSelect) {
        onExampleSelect(content);
      }
    };
  
    return (
      <R2DAccordion title="Try Our Examples" defaultExpanded = "true" icon={<LightbulbIcon />} >
        <ButtonGroup variant="outlined" aria-label="outlined primary button group" sx={{ overflow: 'auto', maxWidth: "100%"}}>
          {mermaidExamples.map((example, index) => (
            <Button key={index} onClick={() => handleExampleSelect(example.content)} sx={{ margin:0.2, fontSize:12}}>
              {example.name}
            </Button>
          ))}
        </ButtonGroup>
      </R2DAccordion>
    );
  }
  
  export default MermaidTemplatesAccordion