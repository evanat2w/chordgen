\layout {
  \context {
    \ChordNames
    \override ChordName #'font-size = #-2
    \override ChordName #'self-alignment-X = #CENTER
    \override ChordName #'X-offset =
      #ly:self-alignment-interface::aligned-on-x-parent
  }
  \context {
    \Staff
    \override TimeSignature #'stencil = ##f
    %% 'in-dot is possible as well:
    \override TextScript.fret-diagram-details.finger-code = #'below-string
    \override TextScript.padding = #4
  }
}

<<
  \new ChordNames \chrds
  \new Staff
    << \fd \m >>
>> 
