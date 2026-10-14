import type { Curriculum } from './types';
export async function loadCurriculum(): Promise<Curriculum> {
  const r = await fetch('/data/lessons.json');
  if (!r.ok) throw new Error(`load failed: ${r.status}`);
  return (await r.json()) as Curriculum;
}
const KEY = 'mcore-academy-progress';
export function getProgress(): Record<string, boolean> {
  try { return JSON.parse(localStorage.getItem(KEY) ?? '{}'); } catch { return {}; }
}
export function toggle(id: string): void {
  const p = getProgress(); p[id] = !p[id];
  localStorage.setItem(KEY, JSON.stringify(p));
}
