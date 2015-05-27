# define-your-dorm

### Installation Instructions (first time)
1. Make sure you have python installed (v2 or v3 will work)
2. If you have already installed virtualenvwrapper and set it up, skip to step 6
3. Run `pip install virtualenvwrapper`. On Linux you might need to `sudo` it but not on Mac.
4. Run `mkdir ~/.virtualenvs`
5. Edit your shell's startup file (`.bashrc`, `.profile`, `.zshrc`, `.bash_profile`, or whatever you use) and add these two lines:
    ```
    export WORKON_HOME=$HOME/.virtualenvs

    source /usr/local/bin/virtualenvwrapper.sh
    ```
6. `cd` to the repository directory if not there, and run `mkvirtualenv define-your-dorm`
7. Run `pip install -r requirements.txt`


### Working on the project (every time)
1. Run `workon define-your-dorm`. This puts you in the virtual environment for this project.
2. If `requirements.txt` has changed recently, re-run `pip install -r requirements.txt` *(make sure you did #1 first)*
3. To start the server, run `python dorm.py` and then go to http://localhost:5000 to access it
4. When you are done, close the terminal or run `deactivate` to leave the virtualenv
