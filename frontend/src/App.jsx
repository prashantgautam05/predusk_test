import { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const ask = async () => {
    const res = await fetch("https://YOUR_BACKEND_URL/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, text })
    });
    setResult(await res.json());
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Mini RAG App</h2>

      <textarea
        placeholder="Paste document (optional)"
        onChange={e => setText(e.target.value)}
      />

      <input
        placeholder="Ask a question"
        onChange={e => setQuery(e.target.value)}
      />

      <button onClick={ask}>Ask</button>

      {result && (
        <>
          <h3>Answer</h3>
          <p>{result.answer}</p>

          <h4>Sources</h4>
          <ul>
            {result.sources.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </>
      )}
    </div>
  );
}

