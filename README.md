# macro
A basic app to define hotkeys, abbreviations and task scheduler, done over a few month. You can consider the app full but it might receive updates/bugfixes in the future (hopefully it doesn't need any bugfixes).
**NOTE**: some apps and games don't work great with it and can detect it as cheating and some antiviruses have false positives since the app don't try at all to hide so use it at your own risk.

# Hotkeys

the current list of action is :
- move the mouse relative and to coordinates
- drag the mouse relative and to coordinates
- click
- open an app with path execpt for the shell or cmd and explorer
- wait
- write
- press a key
- hold and release a key
- scroll vefrtically and horizontally
- press another hotkey
- take a screenshot

By default the ui keybind is ctrl+alt+a but you can change it in the option menu.
You can basically do everything you want with this list but if you think something could be usefull try suggesting it !
Defining a hotkey for an action list is not forced, it's usefull for the task scheduler or turning off a hotkey without deleting it.

# Abbreviation

Very simple, a source (like "@@") that gets replaced by a set text (like your email), usefull for things you type often !

# task scheduler

execute a hotkey (or action list if there's no keys tied to it) at the defined schedule:
- every X minutes
- every days at X hour
- every weeks at X days and hours
- every months at X date and hours
- advanced (used to be more precise or to select multiple schedules)
