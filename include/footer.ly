\layout {
  \context {
    \ChordNames
    \override ChordName #'font-size = #-1
    \override ChordName #'self-alignment-X = #CENTER
    \override ChordName #'X-offset =
      #ly:self-alignment-interface::aligned-on-x-parent
  }
  \context {
    \Staff
    \override BarLine #'stencil = ##f
    \override TimeSignature #'stencil = ##f
    \override TextScript.size = 1.5
    \override TextScript.fret-diagram-details.finger-code = #'below-string
    \override TextScript.fret-diagram-details.number-type = #'arabic
    \override TextScript.fret-diagram-details.fret-label-font-mag = 0.4
    \override TextScript.fret-diagram-details.string-label-font-mag = 0.35
    \override TextScript.fret-diagram-details.dot-color = #'red
    \override TextScript.padding = #4
  }
}

<<
  \new ChordNames \chrds
  \new Staff
    << \fd \m >>
>> 
