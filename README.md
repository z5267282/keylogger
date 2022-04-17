# keylogger
Something Awesome project for COMP6441 22T1.

This program will record user and input data from a computer whilst it is running.
* Keyboard presses
* Mouse clicks

You can run the program via
`python3 keylogger.py`

or use the shell-compiler `generate-exe` to set specific options.

The program will run until `ESC` or the escape key has been hit.

`./generate-exe [-h(elp for how to use the program)]`
* This will generate an executable in both `dist/` and `~/` or the home directory

There is a branch called `testing` where each log is stored

Logs are generated in the same diretory as where the program was run in `logs/`
* Logs are encrypted by default and can be decrypted via `decrypt-json [file]`, generating a decryption in `decrypted.json`
* By default logs are generated every 60 seconds, but this can be overwritten via `generate-exe -i [interval]`

Suffixes determine what is stored in a log file:
* Raw input has no suffix
* Interpreted input (used for password prediction) has the suffix `interpreted`
* Application trackings have `app`
* Predicted passwords if any were found are suffixed in `special`

`pics/` contains any screenshots of research that was later put into the blog posts

