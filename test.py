from pydub import AudioSegment

sound1 = AudioSegment.from_file("input_sound.wav", format="wav")
sound2 = AudioSegment.from_file("output_sound.wav", format="wav")
sound = sound1 + sound2
comfile_handle = sound.export("output.mp3", format="mp3")