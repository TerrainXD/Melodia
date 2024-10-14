import pickle
import numpy
from music21 import instrument, note, stream, chord, tempo
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, BatchNormalization as BatchNorm, Activation

def generate_music(num_notes=500, instrument_name='Piano', speed=1.0):
    """ Generate a midi file with a specific number of notes and instrument """
    with open('backend/datanotes/notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    pitchnames = sorted(set(item for item in notes))
    n_vocab = len(set(notes))

    network_input, normalized_input = prepare_sequences(notes, pitchnames, n_vocab)
    model = create_network(normalized_input, n_vocab)
    prediction_output = generate_notes(model, network_input, pitchnames, n_vocab, num_notes)
    
    midi_file_path = create_midi(prediction_output, instrument_name, speed)
    return midi_file_path


def prepare_sequences(notes, pitchnames, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    sequence_length = 100
    network_input, output = [], []

    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    normalized_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    normalized_input = normalized_input / float(n_vocab)

    return network_input, normalized_input

def create_network(network_input, n_vocab):
    """ Create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(512, input_shape=(network_input.shape[1], network_input.shape[2]), recurrent_dropout=0.3, return_sequences=True))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3))
    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    try:
        model.load_weights('backend/weights-improvement-198-0.2290-bigger.keras')
    except ValueError as e:
        print("Error loading weights:", e)

    return model

def generate_notes(model, network_input, pitchnames, n_vocab, num_notes):
    """ Generate a specific number of notes from the neural network """
    start = numpy.random.randint(0, len(network_input) - 1)
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
    pattern = network_input[start]
    prediction_output = []

    for note_index in range(num_notes):
        prediction_input = numpy.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    return prediction_output

def create_midi(prediction_output, instrument_name, speed):
    """ Convert the output from the prediction to notes and create a midi file """
    offset = 0
    output_notes = []

    # Map instrument name to music21 instrument class
    instrument_map = {
        'Piano': instrument.Piano(),
        'Guitar': instrument.Guitar(),
        'Violin': instrument.Violin()
    }
    chosen_instrument = instrument_map.get(instrument_name, instrument.Piano())  # Default to Piano

    bpm = 120 * speed

    tempo_mark = tempo.MetronomeMark(number=bpm)

    for pattern in prediction_output:
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = chosen_instrument  # Set chosen instrument
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = chosen_instrument  # Set chosen instrument
            output_notes.append(new_note)

        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.insert(0, tempo_mark)
    midi_stream.insert(0, chosen_instrument)  # Insert chosen instrument at the beginning
    midi_file_path = 'backend/static/generated_music.mid'
    midi_stream.write('midi', fp=midi_file_path)
    return midi_file_path

if __name__ == '__main__':
    generate_music()