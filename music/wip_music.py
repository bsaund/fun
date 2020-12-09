import music21
import math



piece = 'C4 F4 G4 C5 B4 G4 F4 E4 D4'
DURATION = 0.3


def convert_to_stream(notes):
    stream = music21.stream.Stream()
    for note_str in notes:
        if note_str == "R":
            stream.append(music21.note.Rest(duration=music21.duration.Duration(DURATION)))
            continue

        note = music21.note.Note(note_str)
        note.duration = music21.duration.Duration(DURATION)
        stream.append(note)
    return stream


def play(notes):
    convert_to_stream(notes).show('midi')


with open('digits_of_pi.txt') as f:
    digits_of_pi = f.readline()


notes = []
for d in digits_of_pi[0:1000]:
    if d == "0":
        notes.append("C3")

    for n in piece.split()[0:int(d)]:
        notes.append(n)

play(piece.split())

print(notes)
play(notes)


# convert_to_stream(piece.split(" ")).show('midi')

# stream = music21.stream.Stream()
# stream.append(f)
# stream.append(music21.note.Note("G4"))
# stream.show('midi')
