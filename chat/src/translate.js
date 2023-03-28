import React, { useState } from "react";
import { translate_to_shakespeare } from "./translator";

function App() {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");

  const handleTranslate = () => {
    const translatedText = translate_to_shakespeare(inputText);
    setOutputText(translatedText);
  };

  return (
    <div>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button onClick={handleTranslate}>Shakespearify</button>
      <textarea value={outputText} readOnly />
    </div>
  );
}

export default App;
