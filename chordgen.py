#!/bin/env python

import json
import abjad

string_map = { "6": 7, "5": 12, "4": 17, "3": 22, "2": 26, "1": 31 }

def get_octave(fret, string, note_name):
    note_number = string_map[string] + int(fret)
    if note_name == "c":
        note_number += 1
    return "'" * int((note_number - 4) // 12.0)

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
    chordno += 1
    chordparts = chord["name"].split(":", 1)
    if len(chordparts) == 1:
        chordparts.append("")
    chrds += "  %s1:%s\n" % (chordparts[0], chordparts[1])
    
    if "notes" not in chord:
        chord["notes"] = ""
        scale = abjad.tonalanalysistools.Scale((str(chordparts[0]), 'major'))
        for fret in [fret for fret in chord["frets"] if fret["fret"] != "x"]:
            next_note = scale.scale_degree_to_named_pitch_class(str(fret["scale_tone"]))
            paren = "\\parenthesize " if "optional" in fret else ""
            chord["notes"] += "%s%s%s " % (paren, next_note.name, get_octave(fret["fret"], fret["string"], next_note.name))

    breakstr = ""
    if chordno % 10 == 0:
        breakstr = "\\break"

    m += "  <%s>1%s\n" % (chord["notes"], breakstr)

    fd += "  s1^\\markup {\n    \\fret-diagram-verbose #`(\n"

    for fret in chord["frets"]:
        if fret["fret"] == "x":
            fd += "      (mute %s)\n" % fret["string"]
            continue

        fd += "      (place-fret %s %s ,#{ \\markup \\fontsize #-3 " % (fret["string"], fret["fret"])

        while fret["scale_tone"][0] not in "0123456789":
            if fret["scale_tone"].startswith("b"):
                fd += "\\with-flat "
            if fret["scale_tone"].startswith("#"):
                fd += "\\with-sharp "
            fret["scale_tone"] = fret["scale_tone"][1:]

        color = "red" if fret["scale_tone"] == "1" else ""
        paren = "parenthesized" if "optional" in fret else ""

        fd += "%s #} %s %s )\n" % (fret["scale_tone"], color, paren)

    if "barres" in chord:
        for barre in chord["barres"]:
            fd += "      (barre %s)\n" % barre

    fd += "  )\n}\n\n"

print "%s\nchrds =\n\\chordmode {\n%s}\n\n" % (ly_header, chrds)
print "m =\n\\absolute {\n  \\override Score.BarNumber.break-visibility = ##(#f #f #f)\n  \\clef \"treble\"\n%s}\n\n" % m 
print "fd = {\n%s}\n\n%s" % (fd, ly_footer)
