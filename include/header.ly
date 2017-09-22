\version "2.19.25"
\language "english"

#(define-markup-command (with-flat layout props text)
   (markup?)
   (interpret-markup layout props
     #{
       \markup \concat { \raise #0.1 \fontsize #-2 \flat $text }
     #}))

#(define-markup-command (with-sharp layout props text)
   (markup?)
   (interpret-markup layout props
     #{
       \markup \concat { \raise #0.3 \fontsize #-5 \sharp $text }
     #}))

chExceptionMusic = {
    <c' e' gs' d''>1-\markup { "+(add9)" }
}

chExceptions = #( append
  ( sequential-music-to-chord-exceptions chExceptionMusic #t)
  ignatzekExceptions)
