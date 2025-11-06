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
      <header className="relative border-b-2 border-primary/20 bg-linear-to-br from-primary/10 via-background to-accent/10 overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0iY3VycmVudENvbG9yIiBzdHJva2Utd2lkdGg9IjAuNSIgb3BhY2l0eT0iMC4xIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] opacity-30" />
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl -translate-y-1/2" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl translate-y-1/2" />
        
        <div className="relative mx-auto max-w-7xl px-4 py-6 sm:px-8 sm:py-8 lg:px-12 lg:py-10">
          <div className="flex items-center gap-4">
            {/* Center content */}
            <div className="flex items-center gap-4 sm:gap-6">
              <div className="relative shrink-0">
                <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full" />
                <div className="relative flex h-14 w-14 sm:h-16 sm:w-16 items-center justify-center rounded-full bg-linear-to-br from-primary/20 to-accent/20 ring-2 ring-primary/30 shadow-xl backdrop-blur-sm">
                  <div className="absolute inset-1.5 rounded-full bg-background/40 backdrop-blur-sm" />
                  <BookOpen className="relative h-7 w-7 sm:h-8 sm:w-8 text-primary drop-shadow-lg" strokeWidth={2} />
                </div>
              </div>
              
              <div>
                <h1 className="font-sans text-2xl sm:text-4xl lg:text-5xl font-black tracking-tight text-transparent bg-clip-text bg-linear-to-r from-foreground via-primary to-foreground">
                  Литературен Архив
                </h1>
                <div className="mt-1 h-0.5 bg-linear-to-r from-primary/60 via-primary/40 to-transparent rounded-full max-w-md" />
                <p className="mt-2 text-xs sm:text-sm text-muted-foreground font-medium">
                  Колекция от литературни произведения с подробен анализ
                </p>
              </div>
            </div>

            {/* Right decorative line */}
            <div className="hidden lg:flex items-center gap-3 flex-1 ml-8">
              <div className="flex gap-1">
                <div className="w-1 h-1 rounded-full bg-accent/20" />
                <div className="w-1 h-1 rounded-full bg-accent/40" />
                <div className="w-1 h-1 rounded-full bg-accent/60" />
              </div>
              <div className="h-px flex-1 bg-linear-to-r from-accent/60 via-accent/40 to-transparent" />
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-8 sm:py-10 lg:px-12 lg:py-14">
        <SearchBar value={searchQuery} onChange={setSearchQuery} />

        <div className="mt-6 sm:mt-10 lg:mt-12 grid gap-6 lg:gap-10 lg:grid-cols-[400px_1fr]">
          <div className="space-y-6">
            <div className="flex items-baseline justify-between border-b border-border/40 pb-3">
              <h2 className="font-serif text-xl sm:text-2xl font-semibold text-foreground">Произведения</h2>
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
                  <p className="mt-6 text-base text-muted-foreground">Изберете произведение за преглед</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
