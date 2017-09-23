\version "2.19.25"
\language "english"

#(define-markup-command (with-flat layout props text)
   (markup?)
   (interpret-markup layout props
     #{
       \markup \concat { \raise #0.3 \fontsize #-4 \flat $text }
     #}))

#(define-markup-command (with-sharp layout props text)
   (markup?)
   (interpret-markup layout props
     #{
       \markup \concat { \raise #0.5 \fontsize #-3 \sharp $text }
     #}))

chExceptionMusic = {
    <c' e' gs' d''>1-\markup { "+(add9)" }
    <c' e' gs' bf' d''>1-\markup { \super "9 #5" }
    <g' b' d'' f'' a'' e'''>1-\markup { \super "13" }
}

chExceptions = #( append
  ( sequential-music-to-chord-exceptions chExceptionMusic #t)
  ignatzekExceptions)

#(define-markup-command (ord layout props text)
   (markup?)
   (interpret-markup layout props
     #{
       \markup \concat { \raise #0.1 \fontsize #-3 \transparent{\flat} $text \transparent{\flat}}
    #}))

%%%%%% scale degrees %%%%%%
".1"   = \markup \ord 1
".2"   = \markup \ord 2
".b3"  = \markup \concat { \with-flat 3 }
".3"   = \markup \ord 3
".4"   = \markup \ord 4
".b5"  = \markup \concat { \with-flat 5 }
".5"   = \markup \ord 5
".#5"  = \markup \concat { \with-sharp 5 }
".b6"  = \markup \concat { \with-flat 6 }
".6"   = \markup \ord 6
".b7"  = \markup \concat { \with-flat 7 }
".bb7" = \markup \concat { \with-flat \with-flat 7 }
".7"   = \markup \ord 7
".b9"  = \markup \concat {\with-flat 9 }
".9"   = \markup \ord 9
".#9"  = \markup \concat { \with-sharp 9 }
".b11" = \markup \concat { \with-flat 11 }
".11"  = \markup \ord 11
".#11" = \markup \concat { \with-sharp 11 }
".13"  = \markup \ord 13
%%%%%%%%%%%%%%%%%%%%%%%%%%%
