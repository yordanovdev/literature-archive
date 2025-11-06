export interface Author {
  name: string;
  year_of_birth: string;
  year_of_death: string;
  information: string;
}

export interface Motif {
  motif_name: string;
  info: string;
}

export interface Theme {
  theme_name: string;
  info: string;
}

export interface Character {
  name: string;
  info: string;
}

export interface Analysis {
  name: string;
  year?: string | undefined;
  genre: string;
  motifs: Motif[];
  themes: Theme[];
  characters: Character[];
  analysis_summary: string;
}

export interface WorkData {
  author: Author;
  analysis: Analysis;
}

export type LiteratureData = WorkData[];
