import customtkinter as ctk
from tkinter import filedialog, messagebox
from music21 import converter, midi
from midi2audio import FluidSynth
import pygame
import os
import threading


class MusicApp:
      def __init__(self, root):
         self.root = root
         self.root.title("MUZTECH-BOT")
         self.root.geometry("500x500")

         self.xml_file = None
         self.sf2_file = None
         self.midi_file = 'output.mid'
         self.audio_file = 'output.wav'

         # Initialisation pygame mixer
         pygame.mixer.init()

         # Creation interface
         self.create_widgets()

      def create_widgets(self):
         
         self.xml_label = ctk.CTkLabel(self.root, text="Entrez votre fichier (.xml ou.mxl):")
         self.xml_label.pack(pady=(20, 0))
         self.xml_entry = ctk.CTkEntry(self.root, width=300)
         self.xml_entry.pack(pady=5)
         self.xml_button = ctk.CTkButton(self.root, text="Repertoire", command=self.load_xml)
         self.xml_button.pack(pady=5)

         
         self.midi_button = ctk.CTkButton(self.root, text="Convertir en MIDI", command=self.start_convert_to_midi)
         self.midi_button.pack(pady=10)

         
         self.sf2_label = ctk.CTkLabel(self.root, text="Votre fichier SoundFont (.sf2):")
         self.sf2_label.pack(pady=(20, 0))
         self.sf2_entry = ctk.CTkEntry(self.root, width=300)
         self.sf2_entry.pack(pady=5)
         self.sf2_button = ctk.CTkButton(self.root, text="Repertoire", command=self.load_sf2)
         self.sf2_button.pack(pady=5)

         # Convert to Audio button
         self.audio_button = ctk.CTkButton(self.root, text="Convertir en Audio", command=self.start_convert_to_audio)
         self.audio_button.pack(pady=10)

         # Progress bar
         self.progress = ctk.CTkProgressBar(self.root)
         self.progress.pack(pady=20)
         self.progress.set(0)

         # Music player controls
         self.play_button = ctk.CTkButton(self.root, text="Play Audio", command=self.play_audio)
         self.play_button.pack(pady=(20, 5))
         self.stop_button = ctk.CTkButton(self.root, text="Stop Audio", command=self.stop_audio)
         self.stop_button.pack(pady=5)

      def load_xml(self):
         self.xml_file = filedialog.askopenfilename(filetypes=[("MusicXML files", "*.xml *.mxl")])
         self.xml_entry.delete(0, ctk.END)
         self.xml_entry.insert(0, self.xml_file)

      def start_convert_to_midi(self):
         threading.Thread(target=self.convert_to_midi).start()

      def convert_to_midi(self):
         if not self.xml_file:
               messagebox.showwarning("Erreur d'entré", "Veuillez entrer votre fichier mxl ou xml.")
               return

         self.progress.set(0.5)
         score = converter.parse(self.xml_file)
         mf = midi.translate.music21ObjectToMidiFile(score)
         mf.open(self.midi_file, 'wb')
         mf.write()
         mf.close()
         self.progress.set(1.0)
         messagebox.showinfo("Conversion Complète", f"Le fichier MIDI a été créé avec succès: {self.midi_file}")
         #os.startfile(self.midi_file)  # Opens the file with the default application

      def load_sf2(self):
         self.sf2_file = filedialog.askopenfilename(filetypes=[("SoundFont files", "*.sf2")])
         self.sf2_entry.delete(0, ctk.END)
         self.sf2_entry.insert(0, self.sf2_file)

      def start_convert_to_audio(self):
         threading.Thread(target=self.convert_to_audio).start()

      def convert_to_audio(self):
         if not self.sf2_file:
               messagebox.showwarning("Erreur", "Veuillez entré votre Soundfont.")
               return

         self.progress.set(0.5)
         fs = FluidSynth(self.sf2_file)
         fs.midi_to_audio(self.midi_file, self.audio_file)
         self.progress.set(1.0)
         messagebox.showinfo("Conversion Complète", f"Le fichier audio a été créé avec succès:{self.audio_file}")
         #os.startfile(self.audio_file)  # Opens the file with the default application

      def play_audio(self):
         if not os.path.exists(self.audio_file):
               messagebox.showwarning("Erreur du Fichier", "Le fichier audio n'est pas trouvé. Veuillez convertir en prémier le Fichier.")
               return

         pygame.mixer.music.load(self.audio_file)
         pygame.mixer.music.play()

      def stop_audio(self):
         pygame.mixer.music.stop()

if __name__ == "__main__":
   # Set appearance and color theme
   ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
   ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

   root = ctk.CTk()  # Correct instantiation of the main window
   app = MusicApp(root)
   root.mainloop()

