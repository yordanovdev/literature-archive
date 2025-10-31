"use client"

import type { WorkData } from "@/lib/types"
import { BookMarked } from "lucide-react"

interface WorksListProps {
  works: WorkData[]
  onSelectWork: (work: WorkData) => void
  selectedWork: WorkData | null
}

export function WorksList({ works, onSelectWork, selectedWork }: WorksListProps) {
  return (
    <div className="space-y-3">
      {works.map((work, index) => (
        <button
          key={index}
          onClick={() => onSelectWork(work)}
          className={`group w-full text-left transition-all duration-200 ${
            selectedWork === work
              ? "bg-primary/5 ring-2 ring-primary/30"
              : "bg-card hover:bg-card/80 ring-1 ring-border/60 hover:ring-primary/40"
          } rounded-xl p-5 shadow-sm hover:shadow-md`}
        >
          <div className="flex items-start gap-4">
            <div
              className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-lg transition-colors ${
                selectedWork === work ? "bg-primary/15 text-primary" : "bg-muted/80 text-muted-foreground/70"
              }`}
            >
              <BookMarked className="h-5 w-5" strokeWidth={1.5} />
            </div>
            <div className="flex-1 min-w-0">
              <h3
                className={`text-lg font-bold leading-tight transition-colors ${
                  selectedWork === work ? "text-primary" : "text-foreground group-hover:text-primary"
                }`}
              >
                {work.analysis.name}
              </h3>
              <p className="mt-1.5 text-sm text-muted-foreground line-clamp-1">{work.author.name}</p>
              {work.analysis.year && (
                <p className="mt-1 text-xs font-medium text-muted-foreground/70">{work.analysis.year}</p>
              )}
            </div>
          </div>
        </button>
      ))}
    </div>
  )
}
