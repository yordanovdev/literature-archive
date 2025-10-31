"use client"

import { Card } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import type { Author, Work } from "@/lib/types"
import { User } from "lucide-react"

interface AuthorListProps {
  authors: Author[]
  onSelectWork: (work: Work) => void
  onSelectAuthor: (author: Author) => void
  selectedWork: Work | null
}

export function AuthorList({ authors, onSelectWork, onSelectAuthor, selectedWork }: AuthorListProps) {
  return (
    <div className="space-y-4">
      {authors.map((author) => (
        <Card
          key={author.id}
          className="overflow-hidden border border-border/60 bg-card shadow-sm hover:shadow-md transition-all duration-300"
        >
          <Accordion type="single" collapsible>
            <AccordionItem value={author.id} className="border-0">
              <AccordionTrigger className="px-4 sm:px-6 py-4 sm:py-5 hover:no-underline hover:bg-muted/50 transition-colors group">
                <div className="text-left flex-1">
                  <div className="font-serif text-lg sm:text-xl font-semibold text-foreground text-balance group-hover:text-primary transition-colors">
                    {author.name}
                  </div>
                  <div className="mt-1.5 sm:mt-2 text-xs sm:text-sm text-muted-foreground">{author.period}</div>
                </div>
              </AccordionTrigger>
              <AccordionContent className="px-4 sm:px-6 pb-6">
                <Button
                  onClick={() => onSelectAuthor(author)}
                  variant="outline"
                  size="sm"
                  className="mb-4 w-full justify-start gap-2 border-accent/40 hover:bg-accent/10 hover:border-accent"
                >
                  <User className="h-4 w-4" />
                  View Author Details
                </Button>

                <p className="mb-6 text-sm text-muted-foreground leading-relaxed border-l-2 border-accent/30 pl-4 py-2">
                  {author.bio}
                </p>
                <div className="space-y-2">
                  <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Works</div>
                  {author.works.map((work) => (
                    <button
                      key={work.id}
                      onClick={() => onSelectWork(work)}
                      className={`group w-full rounded-xl px-5 py-4 text-left transition-all duration-200 border-2 ${
                        selectedWork?.id === work.id
                          ? "bg-primary text-primary-foreground shadow-lg ring-2 ring-primary/30 border-primary scale-[1.02]"
                          : "bg-card hover:bg-accent/20 text-foreground hover:shadow-md border-border/60 hover:border-accent hover:scale-[1.01]"
                      }`}
                    >
                      <div className="font-serif text-base font-semibold group-hover:text-primary transition-colors">
                        {work.title}
                      </div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        {work.year} • {work.literaryAge}
                      </div>
                    </button>
                  ))}
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </Card>
      ))}
    </div>
  )
}
