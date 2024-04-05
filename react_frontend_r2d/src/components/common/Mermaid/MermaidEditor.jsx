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
  scrollBeyondLastLine:false,
};

const MermaidEditor = ({ mermaidCode, onCodeChange }) => {
  const editorDidMount = (editor, monaco) => {
    editor.focus();
  };

  return (
    <div style={{width: '100%', height: '100%', overflow:'hidden' }}>
    <MonacoEditor
      height="100%" 
      width="100%"
      language="yaml" 
      value={mermaidCode}
      options={options}
      onChange={onCodeChange}
      editorDidMount={editorDidMount}
    />
    </div>
  );
};

export default MermaidEditor;
