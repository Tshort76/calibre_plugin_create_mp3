# How to Package and Install
See https://manual.calibre-ebook.com/creating_plugins.html for more details
## Create plugin directory
Zip the `*.py`,`*.txt`, and `*.png` files in this project into a zip.

## Install
In Calibre, go to Preferences -> Advanced -> Plugins -> `Load plugin from file` and select the ZIP file from step 1.

## Configuration
Running the Plugin will show a `Configure` button, which allows you to configure the RUN COMMAND.

### RUN COMMAND
The plugin assumes that you are able to specify a shell command that can be executed to convert a book at path :BOOK: into an mp3 file.

The plugin assumes that your script takes at least 1 parameter corresponding to the absolute filepath to the book.  This is specified in you run command by inserting a `:BOOK:` placeholder to represent where the book's path should be passed into the command (e.g. the first positional argment).  When the script is executed, the Calibre plugin will substitute the book's actual path into the command.

Similarly, you can pass the book's associated meta data from Calibre by placing `:META:` in the command.

#### Examples
---------------------------
`python generate_mp3.py true :BOOK: Sonia_GB --speed 2`

`/users/bob/dev/gen_mp3/.venv/scripts/python /users/bob/dev/gen_mp3/generate_mp3.py :BOOK: --voice en-CA-ClaraNeural --speed 2 -m :META:`

### Using Echo
If you do not have a way favorite TTS engine, you can use the https://github.com/Tshort76/echo library, which leverages Microsoft's `edge-tts` server for text-to-speech.

The run command for echo is something like:

`\path\to\echo\.venv\Scripts\python \path\to\echo\create_audio.py :BOOK: -v en-GB-RyanNeural -s 1.25 -m :META: --save`

#### Voices
Visit https://tts.travisvn.com/ to hear sample recordings of the voices available through edge-tts