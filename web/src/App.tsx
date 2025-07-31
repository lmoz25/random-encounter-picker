import { useState } from 'react';
import encounters from './encounters.json';
import encounterTextsData from './encounter_texts.json';
import './App.css';

interface Encounter {
  number: number;
  title: string;
  page: number | null;
}

// Add index signature for dynamic access
const encounterTexts = encounterTextsData as Record<string, string>;

function getEncounterBody(title: string): string | undefined {
  // Try exact match first
  if (encounterTexts[title]) return encounterTexts[title];
  // Try matching by first word (for cases like "Noosed 14")
  const firstWord = title.split(' ')[0];
  return encounterTexts[firstWord];
}

function App() {
  const [selected, setSelected] = useState<Encounter | null>(null);

  function pickRandom() {
    const idx = Math.floor(Math.random() * encounters.length);
    setSelected(encounters[idx]);
  }

  const body = selected ? getEncounterBody(selected.title) : undefined;

  return (
    <div className="container">
      <h1>Random D&D Road Encounter</h1>
      <button onClick={pickRandom} className="pick-btn">Pick Encounter</button>
      {selected && (
        <div className="encounter-card">
          <h2>#{selected.number}: {selected.title}</h2>
          {body ? (
            <pre style={{ textAlign: 'left', whiteSpace: 'pre-wrap', marginTop: '1em' }}>{body}</pre>
          ) : (
            <p><em>No body text found for this encounter.</em></p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
