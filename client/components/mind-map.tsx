"use client"

import { useMemo, useState } from "react"
import type { WorkData } from "@/lib/types"
import { Badge } from "@/components/ui/badge"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface MindMapProps {
  work: WorkData
}

interface DetailItem {
  type: "theme" | "motif" | "character"
  name: string
  info: string
}

export function MindMap({ work }: MindMapProps) {
  const [selectedItem, setSelectedItem] = useState<DetailItem | null>(null)

  const data = useMemo(() => {
    return {
      title: work.analysis.name,
      author: `${work.author.name} (${work.author.year_of_birth}–${work.author.year_of_death})`,
      year: work.analysis.year,
      genre: work.analysis.genre,
      themes: work.analysis.themes?.map(t => t.theme_name) || [],
      motifs: work.analysis.motifs?.map(m => m.motif_name) || [],
      characters: work.analysis.characters?.map(c => c.name) || [],
    }
  }, [work])

  const handleItemClick = (type: "theme" | "motif" | "character", name: string) => {
    let info = ""
    if (type === "theme") {
      const theme = work.analysis.themes?.find(t => t.theme_name === name)
      info = theme?.info || ""
    } else if (type === "motif") {
      const motif = work.analysis.motifs?.find(m => m.motif_name === name)
      info = motif?.info || ""
    } else if (type === "character") {
      const character = work.analysis.characters?.find(c => c.name === name)
      info = character?.info || ""
    }
    setSelectedItem({ type, name, info })
  }

  const getTypeLabel = (type: "theme" | "motif" | "character") => {
    switch (type) {
      case "theme": return "Тема"
      case "motif": return "Мотив"
      case "character": return "Герой"
    }
  }

  const getTypeColor = (type: "theme" | "motif" | "character") => {
    switch (type) {
      case "theme": return "text-primary"
      case "motif": return "text-accent"
      case "character": return "text-chart-1"
    }
  }

  return (
    <div className="relative">
      {/* Central node */}
      <div className="flex justify-center mb-8">
        <div className="relative">
          <div className="rounded-2xl border-2 border-primary bg-primary/5 px-8 py-6 text-center shadow-lg backdrop-blur-sm">
            <p className="text-xs uppercase tracking-[0.25em] text-muted-foreground font-medium">Литературно Произведение</p>
            <h4 className="mt-2 text-2xl font-bold text-foreground">{data.title}</h4>
            <p className="mt-2 text-sm text-muted-foreground">{data.author}</p>
            <div className="mt-3 flex items-center justify-center gap-2">
              {data.year && (
                <Badge variant="secondary" className="text-xs">
                  {data.year}
                </Badge>
              )}
              {data.genre && (
                <Badge variant="outline" className="text-xs">
                  {data.genre}
                </Badge>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Branches */}
      <div className="grid gap-6 md:grid-cols-3">
        {/* Themes */}
        {data.themes.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="h-8 w-1 rounded-full bg-linear-to-b from-primary to-primary/40" />
              <h5 className="font-semibold text-lg text-foreground">Теми</h5>
            </div>
            <div className="pl-4 space-y-2">
              {data.themes.map((theme, index) => (
                <button
                  key={index}
                  onClick={() => handleItemClick("theme", theme)}
                  className="w-full group relative rounded-lg border border-primary/20 bg-primary/5 px-4 py-2.5 transition-all hover:border-primary/40 hover:bg-primary/10 hover:shadow-md cursor-pointer"
                >
                  <div className="flex items-start gap-2">
                    <div className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-primary group-hover:scale-125 transition-transform" />
                    <p className="text-sm font-medium text-foreground leading-snug text-left">{theme}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Motifs */}
        {data.motifs.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="h-8 w-1 rounded-full bg-linear-to-b from-accent to-accent/40" />
              <h5 className="font-semibold text-lg text-foreground">Мотиви</h5>
            </div>
            <div className="pl-4 space-y-2">
              {data.motifs.map((motif, index) => (
                <button
                  key={index}
                  onClick={() => handleItemClick("motif", motif)}
                  className="w-full group relative rounded-lg border border-accent/20 bg-accent/5 px-4 py-2.5 transition-all hover:border-accent/40 hover:bg-accent/10 hover:shadow-md cursor-pointer"
                >
                  <div className="flex items-start gap-2">
                    <div className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-accent group-hover:scale-125 transition-transform" />
                    <p className="text-sm font-medium text-foreground leading-snug text-left">{motif}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Characters */}
        {data.characters.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="h-8 w-1 rounded-full bg-linear-to-b from-chart-1 to-chart-1/40" />
              <h5 className="font-semibold text-lg text-foreground">Герои</h5>
            </div>
            <div className="pl-4 space-y-2">
              {data.characters.map((character, index) => (
                <button
                  key={index}
                  onClick={() => handleItemClick("character", character)}
                  className="w-full group relative rounded-lg border border-chart-1/20 bg-chart-1/5 px-4 py-2.5 transition-all hover:border-chart-1/40 hover:bg-chart-1/10 hover:shadow-md cursor-pointer"
                >
                  <div className="flex items-start gap-2">
                    <div className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-chart-1 group-hover:scale-125 transition-transform" />
                    <p className="text-sm font-medium text-foreground leading-snug text-left">{character}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Detail Dialog */}
      <Dialog open={!!selectedItem} onOpenChange={() => setSelectedItem(null)}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          {selectedItem && (
            <>
              <DialogHeader>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <DialogTitle className="text-2xl font-bold text-foreground pr-8">
                      {selectedItem.name}
                    </DialogTitle>
                    <DialogDescription className={`mt-2 text-sm font-medium uppercase tracking-wider ${getTypeColor(selectedItem.type)}`}>
                      {getTypeLabel(selectedItem.type)}
                    </DialogDescription>
                  </div>
                </div>
              </DialogHeader>
              <div className="mt-6">
                <div className="rounded-lg border border-border/60 bg-muted/30 p-6">
                  <p className="text-sm text-foreground leading-relaxed whitespace-pre-line">
                    {selectedItem.info}
                  </p>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}
