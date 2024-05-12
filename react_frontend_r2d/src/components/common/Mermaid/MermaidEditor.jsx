import React, {useState} from 'react';
import MonacoEditor from 'react-monaco-editor';

const options = {
  selectOnLineNumbers: true,
  roundedSelection: false,
  readOnly: false,
  cursorStyle: 'line',
  automaticLayout: true,
  fontSize: 19,
  scrollBeyondLastLine:true,
};

const MermaidEditor = ({ mermaidCode, onCodeChange }) => {

  const [isEditorFocused, setEditorFocused] = useState(false);

  const editorDidMount = (editor, monaco) => {
    editor.onDidFocusEditorWidget(() => {
      editor.focus(true)
      setEditorFocused(true); // Editor is focused, disable page scroll
    });

    editor.onDidBlurEditorWidget(() => {
      setEditorFocused(false); // Editor is blurred, enable page scroll
    });
  };

  return (
    <div style={{width: '100%', height: '100%', overflow:'hidden' }}>
    <MonacoEditor
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
