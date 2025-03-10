import React from 'react';
import MonacoEditor from 'react-monaco-editor';

const read_only_options = {
  selectOnLineNumbers: true,
  roundedSelection: true,
  readOnly: true,
  cursorStyle: 'hidden',
  automaticLayout: true,
  theme: 'vs',
  fontSize: 14,
  scrollBeyondLastLine:true,
};

// MonacoEditor maps file extensions to a language, populate this map so that MonacoEditor can prettify content.
const fileExtensionToLanguageMap = {
    'application/json': 'json',
    'text/plain': 'plaintext',
    'md': 'markdown',
    'mermaid':'yaml'
}

const ReadOnlyEditor = ({ fileExtension, fileContents }) => {
  const language = fileExtensionToLanguageMap[fileExtension] || 'plaintext'; // Default to plaintext if no mapping found
  const editorDidMount = (editor, _) => {
    editor.focus();
};

  return (
    <div style={{width: '100%', height: '100%', overflow:'hidden'}}>
    <MonacoEditor
      height="100%" 
      width="100%"
      language="json"
      value={fileContents}
      options={read_only_options}
      editorDidMount={editorDidMount}
    />
    </div>
  );
};

export default ReadOnlyEditor;
