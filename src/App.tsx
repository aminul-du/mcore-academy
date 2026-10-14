import { useEffect, useState } from 'react';
import { loadCurriculum, getProgress, toggle } from './api';
import type { Curriculum } from './types';

export default function App() {
  const [data, setData] = useState<Curriculum | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [progress, setProgress] = useState<Record<string,boolean>>({});
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    loadCurriculum().then((c) => {
      setData(c); setProgress(getProgress());
      setSelected(c.lessons[0]?.id ?? null);
    }).catch((e) => setErr(e.message));
  }, []);

  if (err) return <main style={{padding:'2rem'}}><h1>MCore Academy</h1><p style={{color:'#f87171'}}>Load failed: {err}</p></main>;
  if (!data) return <main style={{padding:'2rem'}}><p>Loading…</p></main>;

  const lesson = data.lessons.find((l) => l.id === selected) ?? null;
  const lm = new Map(data.lessons.map((l) => [l.id, l]));
  const done = Object.values(progress).filter(Boolean).length;

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand"><h1>MCore Academy</h1><p className="muted small">Engineering Intelligence for the World</p></div>
        <div className="prog"><div className="track"><div className="fill" style={{width:`${(done/data.lessons.length)*100}%`}}/></div><p className="muted small">{done} / {data.lessons.length} complete</p></div>
        <nav>
          {data.meta.modules.map((m) => (
            <div key={m.id} className="mod">
              <div className="mod-title">{m.title}</div>
              <ul>{m.lessons.map((id,i) => {
                const l = lm.get(id); if (!l) return null;
                const active = selected === id; const isDone = progress[id];
                return (<li key={id}><button className={`lesson-link ${active?'active':''} ${isDone?'done':''}`} onClick={()=>setSelected(id)}>
                  <span className="num">{String(i+1).padStart(2,'0')}</span>
                  <span className="lt">{l.title}</span>
                  {isDone && <span className="check">✓</span>}
                </button></li>);
              })}</ul>
            </div>
          ))}
        </nav>
      </aside>
      <main className="content">
        {lesson ? (
          <article className="lesson">
            <header>
              <div className="tags">{lesson.tags.map(t=><span key={t} className="tag">{t}</span>)}</div>
              <h2>{lesson.title}</h2><p className="muted">{lesson.summary}</p>
              <button className={`done-btn ${progress[lesson.id]?'done':''}`} onClick={()=>{toggle(lesson.id);setProgress(getProgress());}}>
                {progress[lesson.id] ? '✓ Marked complete' : 'Mark complete'}
              </button>
            </header>
            <div className="body">{lesson.content.map((b,i) => {
              if (b.type==='h')    return <h3 key={i}>{b.text}</h3>;
              if (b.type==='p')    return <p key={i}>{b.text}</p>;
              if (b.type==='list') return <ul key={i}>{b.items?.map((x,j)=><li key={j}>{x}</li>)}</ul>;
              if (b.type==='code') return <pre key={i} className="code"><code>{b.code}</code></pre>;
              if (b.type==='note') return <div key={i} className="note">{b.text}</div>;
              return null;
            })}</div>
          </article>
        ) : <p className="muted" style={{padding:'2rem'}}>Select a lesson.</p>}
      </main>
    </div>
  );
}
