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

The shell command to do this should be specified using the :BOOK: placeholder to represent where the book's path should be passed into the command.  Similarly, you can pass the book's associated meta data by placing :META: in the command.

Command path examples
---------------------------
`python generate_mp3.py true :BOOK: Sonia_GB --speed 2`

`/users/bob/dev/gen_mp3/.venv/scripts/python /users/bob/dev/gen_mp3/generate_mp3.py :BOOK: --voice Sonia_GB --speed 2 -m :META:`
