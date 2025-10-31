import { Card } from "@/components/ui/card"
import type { WorkData } from "@/lib/types"
import { User } from "lucide-react"

interface WorkDetailProps {
  work: WorkData
}

export function WorkDetail({ work }: WorkDetailProps) {
  return (
    <div className="space-y-8">
      <div className="border-b border-border/40 pb-6">
        <h2 className="font-mono text-4xl sm:text-5xl font-bold text-foreground text-balance leading-tight">
          {work.analysis.name}
        </h2>
        {work.analysis.year && (
          <div className="mt-3 text-sm text-muted-foreground">
            <span className="font-medium text-accent">{work.analysis.year}</span>
          </div>
        )}
      </div>

      <Card className="p-6 sm:p-8 shadow-sm border border-border/60 bg-card/50">
        <div className="flex items-start gap-4 mb-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
            <User className="h-5 w-5 text-primary" strokeWidth={1.5} />
          </div>
          <div>
            <h3 className="font-mono text-2xl font-semibold text-foreground">{work.author.name}</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              {work.author.year_of_birth} – {work.author.year_of_death}
            </p>
          </div>
        </div>
        <p className="text-sm text-muted-foreground leading-relaxed">{work.author.information}</p>
      </Card>

      {work.analysis.themes && work.analysis.themes.length > 0 && (
        <Card className="p-6 sm:p-8 shadow-sm border border-border/60 bg-card">
          <h3 className="mb-6 font-mono text-2xl font-semibold text-foreground">Themes</h3>
          <div className="space-y-6">
            {work.analysis.themes.map((theme, index) => (
              <div key={index} className="border-l-4 border-primary/30 pl-6 py-2">
                <div className="font-semibold text-lg text-foreground mb-2">{theme.theme_name}</div>
                <p className="text-sm text-muted-foreground leading-relaxed">{theme.info}</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {work.analysis.motifs && work.analysis.motifs.length > 0 && (
        <Card className="p-6 sm:p-8 shadow-sm border border-border/60 bg-card">
          <h3 className="mb-6 font-mono text-2xl font-semibold text-foreground">Motifs</h3>
          <div className="space-y-6">
            {work.analysis.motifs.map((motif, index) => (
              <div key={index} className="border-l-4 border-accent/40 pl-6 py-2">
                <div className="font-semibold text-lg text-foreground mb-2">{motif.motif_name}</div>
                <p className="text-sm text-muted-foreground leading-relaxed">{motif.info}</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {work.analysis.characters && work.analysis.characters.length > 0 && (
        <Card className="p-6 sm:p-8 shadow-sm border border-border/60 bg-card">
          <h3 className="mb-6 font-mono text-2xl font-semibold text-foreground">Characters</h3>
          <div className="space-y-6">
            {work.analysis.characters.map((character, index) => (
              <div key={index} className="border-l-4 border-primary/30 pl-6 py-2">
                <div className="font-semibold text-lg text-foreground mb-2">{character.name}</div>
                <p className="text-sm text-muted-foreground leading-relaxed">{character.info}</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {work.analysis.analysis_summary && (
        <Card className="p-6 sm:p-8 shadow-sm border border-border/60 bg-card">
          <h3 className="mb-6 font-mono text-2xl font-semibold text-foreground">Analysis</h3>
          <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
            {work.analysis.analysis_summary}
          </p>
        </Card>
      )}
    </div>
  )
}
