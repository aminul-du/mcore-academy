export interface Block { type:'p'|'h'|'list'|'code'|'note'; text?:string; items?:string[]; code?:string; }
export interface Lesson { id:string; title:string; tags:string[]; summary:string; content:Block[]; }
export interface Module { id:string; title:string; lessons:string[]; }
export interface Curriculum { meta:{ title:string; version:string; modules:Module[] }; lessons:Lesson[]; }
