#!/bin/env python

import json
import abjad

string_map = { "6": 3, "5": 8, "4": 13, "3": 18, "2": 22, "1": 27 }

def get_octave(fret, string, note):
    note_number = string_map[str(string)] + int(fret)
    num_octaves = int(note_number // 12.0)
    if (note.name.startswith("c") and not note.name.startswith("cs")) or (note.name == "dff"):
        num_octaves += 1
    return "'" * num_octaves

header_file = open("include/header.ly", "r")
ly_header = header_file.read()

footer_file = open("include/footer.ly", "r")
ly_footer = footer_file.read()

with open('chords.json') as chords_file:
    data = json.load(chords_file)

chrds = ""
m = ""
fd = ""

chordno = 0
for chord in data["chords"]:
    if chord["name"] == "break":
        m += "  \\break\n"
        chordno = 0
        continue

    chordno += 1
    chord_notes = ""

    # Split the chord name at the : and add a whole note duration (d:m -> d1:m)
    chordparts = chord["name"].split(":", 1)
    if len(chordparts) == 1:
        chordparts.append("")
    chrds += "  %s1:%s\n" % (chordparts[0], chordparts[1])
    
    scale = abjad.tonalanalysistools.Scale((str(chordparts[0]), 'major'))

    fd += "  %%%s\n  s1^\\markup {\n    \\fret-diagram-verbose #`(\n" % chord["name"]

    if "barres" in chord:
        for barre in chord["barres"]:
            fd += "      (barre %s)\n" % barre

    string_no = 7
    for frets in chord["frets"].split(";"):
        string_no -= 1
        for fret in frets.split(","):
            optional = False

            if fret == "x":
                fd += "      (mute %d)\n" % string_no
                continue

            (fret_no, scale_tone) = fret.split("-")
            if scale_tone.startswith("o"):
                optional = True
                scale_tone = scale_tone[1:]

            next_note = scale.scale_degree_to_named_pitch_class(str(scale_tone))

            color = "red " if scale_tone == "1" else ""
            paren = "parenthesized " if optional else ""

            fd += "      (place-fret %d %s ,#{ \\\".%s\" #} %s%s)\n" % (string_no, fret_no, scale_tone, color, paren)

            paren = "\\parenthesize " if optional else ""
            chord_notes += "%s%s%s " % (paren, next_note.name, get_octave(fret_no, string_no, next_note))

    fd += "  )\n}\n\n"

    breakstr = ""
    if chordno % 8 == 0:
        breakstr = "\n  \\break"

    m += "  <%s>1 %%%s%s\n" % (chord_notes, chord["name"], breakstr)

print "%s\nchrds =\n\\chordmode {\n  \\set chordNameExceptions = #chExceptions\n%s}\n\n" % (ly_header, chrds)
print "m =\n\\absolute {\n  \\override Score.BarNumber.break-visibility = ##(#f #f #f)\n  \\clef \"treble\"\n%s}\n\n" % m 
print "fd = {\n%s}\n\n%s" % (fd, ly_footer)
