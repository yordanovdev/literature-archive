"use client"

import { useState, useRef } from "react"
import { WorksList } from "@/components/works-list"
import { WorkDetail } from "@/components/work-detail"
import { SearchBar } from "@/components/search-bar"
import { sampleData } from "@/lib/sample-data"
import type { WorkData } from "@/lib/types"
import { BookOpen } from "lucide-react"

export default function Page() {
  const [works] = useState<WorkData[]>(sampleData)
  const [selectedWork, setSelectedWork] = useState<WorkData | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const workDetailRef = useRef<HTMLDivElement>(null)

  const filteredWorks = works.filter((work) => {
    const query = searchQuery.toLowerCase()
    const workMatch = work.analysis.name.toLowerCase().includes(query)
    const authorMatch = work.author.name.toLowerCase().includes(query)
    const themeMatch = work.analysis.themes.some(
      (t) => t.theme_name.toLowerCase().includes(query) || t.info.toLowerCase().includes(query),
    )
    const motifMatch = work.analysis.motifs.some(
      (m) => m.motif_name.toLowerCase().includes(query) || m.info.toLowerCase().includes(query),
    )
    return workMatch || authorMatch || themeMatch || motifMatch
  })

  const handleSelectWork = (work: WorkData) => {
    setSelectedWork(work)
    
    // Scroll to work detail on mobile
    if (workDetailRef.current && window.innerWidth < 1024) {
      setTimeout(() => {
        workDetailRef.current?.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start' 
        })
      }, 100)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border/60 bg-card/80 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-8 sm:py-8 lg:px-12 lg:py-12">
          <div className="flex items-start gap-3 sm:gap-6">
            <div className="flex h-10 w-10 sm:h-14 sm:w-14 items-center justify-center rounded-xl sm:rounded-2xl bg-primary/10 ring-1 ring-primary/20">
              <BookOpen className="h-5 w-5 sm:h-7 sm:w-7 text-primary" strokeWidth={1.5} />
            </div>
            <div className="flex-1">
              <h1 className="font-serif text-2xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-foreground text-balance">
                Literary Archive
              </h1>
              <p className="mt-1 sm:mt-2 text-xs sm:text-sm text-muted-foreground max-w-2xl leading-relaxed">
                A curated collection of literary works with comprehensive analysis
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-8 sm:py-10 lg:px-12 lg:py-14">
        <SearchBar value={searchQuery} onChange={setSearchQuery} />

        <div className="mt-6 sm:mt-10 lg:mt-12 grid gap-6 lg:gap-10 lg:grid-cols-[400px_1fr]">
          <div className="space-y-6">
            <div className="flex items-baseline justify-between border-b border-border/40 pb-3">
              <h2 className="font-serif text-xl sm:text-2xl font-semibold text-foreground">Works</h2>
              <span className="text-sm font-medium text-primary">{filteredWorks.length}</span>
            </div>
            <WorksList works={filteredWorks} onSelectWork={handleSelectWork} selectedWork={selectedWork} />
          </div>

          <div ref={workDetailRef}>
            {selectedWork ? (
              <WorkDetail work={selectedWork} />
            ) : (
              <div className="flex h-[600px] items-center justify-center rounded-2xl border-2 border-dashed border-border/40 bg-muted/30">
                <div className="text-center">
                  <BookOpen className="mx-auto h-16 w-16 text-muted-foreground/30" strokeWidth={1.5} />
                  <p className="mt-6 text-base text-muted-foreground">Select a work to view details</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
