import React from 'react';
import MonacoEditor from 'react-monaco-editor';


const options = {
  selectOnLineNumbers: true,
  roundedSelection: false,
  readOnly: false,
  cursorStyle: 'line',
  automaticLayout: true,
  theme: 'vs',
  fontSize: 19,
};

const MermaidEditor = ({ mermaidCode, onCodeChange }) => {
  const editorDidMount = (editor, monaco) => {
    editor.focus();
  };

  return (
    <MonacoEditor
      height="100%" 
      width="100%"
      language="yaml" 
      value={mermaidCode}
      options={options}
      onChange={onCodeChange}
      editorDidMount={editorDidMount}
    />
  );
};

export default MermaidEditor;
