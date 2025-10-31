import { Card } from "@/components/ui/card"
import type { Author } from "@/lib/types"
import { User, Calendar, BookOpen } from "lucide-react"

interface AuthorDetailProps {
  author: Author
}

export function AuthorDetail({ author }: AuthorDetailProps) {
  return (
    <div className="space-y-8">
      <Card className="overflow-hidden border border-border/60 bg-card shadow-sm">
        <div className="bg-gradient-to-br from-primary/10 via-accent/10 to-primary/5 px-8 py-10 border-b border-border/60">
          <div className="flex items-start gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/20 ring-2 ring-primary/30">
              <User className="h-8 w-8 text-primary" strokeWidth={1.5} />
            </div>
            <div className="flex-1">
              <h2 className="font-serif text-4xl font-bold text-foreground text-balance">{author.name}</h2>
              <div className="mt-3 flex items-center gap-2 text-sm text-muted-foreground">
                <Calendar className="h-4 w-4" />
                <span>{author.period}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="px-8 py-8">
          <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">Biography</h3>
          <p className="text-base leading-relaxed text-foreground">{author.bio}</p>
        </div>
      </Card>

      <Card className="overflow-hidden border border-border/60 bg-card shadow-sm">
        <div className="px-8 py-6 border-b border-border/40">
          <div className="flex items-center gap-3">
            <BookOpen className="h-5 w-5 text-primary" strokeWidth={1.5} />
            <h3 className="font-serif text-2xl font-semibold text-foreground">Works</h3>
            <span className="ml-auto text-sm font-medium text-primary">{author.works.length}</span>
          </div>
        </div>
        <div className="px-8 py-6">
          <div className="space-y-4">
            {author.works.map((work) => (
              <div
                key={work.id}
                className="rounded-xl border-2 border-border/60 bg-muted/30 px-6 py-5 hover:border-accent hover:bg-accent/10 transition-all duration-200"
              >
                <div className="font-serif text-xl font-semibold text-foreground">{work.title}</div>
                <div className="mt-2 flex items-center gap-4 text-sm text-muted-foreground">
                  <span className="font-medium">{work.year}</span>
                  <span className="text-border">•</span>
                  <span>{work.literaryAge}</span>
                </div>
                {work.theme && work.theme.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {work.theme.map((theme, idx) => (
                      <span
                        key={idx}
                        className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary ring-1 ring-primary/20"
                      >
                        {theme.name}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  )
}
