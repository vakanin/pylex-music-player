# pylex-music-player
	This is simple music player with everything that should have one player.

# Requirements
	- Qt4 or maybe older :)
	- PyQt/PySide
	- Python 3.4+
	- mutagen
	- you must have some music files on your computer :)

# Python3 installation for Linux(Ubuntu)
	- sudo apt-get install python3-minimal

# PySide installation for Linux(Ubuntu)
	- sudo apt-get install python3-pyside

# Mutagen installation
	- pip3 install mutagen

# Installation
	git clone https://github.com/vakanin/pylex-music-player.git
	python3 player.py

# Usage
	1. add some files with songs in the player
	2. click "Play" button
	3. just listen your favourite songs and have fun :)

# How to ?

## How to add new song ?
	click on File-->Open and select the song/songs you want.

## How to play song ?
	click on button Play or double click on song in playlist

## How to stop song ?
	click on button Stop

## How to pause song ?
	click on button Pause while the song is playing

## How to play next or previous song ?
	click on button >> for next song or click on button << for previous song

## How to sort by ... ?
	You can sort by many categories as title, artist name, filename and year.
	You can do this by clicking on Playlist-->Sort and from context menu choose the category.

## How to shuffle the playlist ?
	You click on Playlist-->Shuffle or Alt + P + S

## How to increase/decrease volume?
	There is volume slider and you can volume up or down with moving a volume slider left or righ

## How to mute ?
	click on button mute (on the left side of volume slider)

## How to tumble(jump) in song ?
	just drag time slider left or right

## How to turn ON random mode ?
	just click on random check box

## How to turn ON repeat mode ?
	just click on repeat check box

## How to clear playlist ?
	click on Playlist-->Clear

## How to search in playlist ?
	click on Playlist-->Search

## How to exit the player ?
	click on File-->Quit or click on button Exit

# Documentation

## class AudioPlayer
	AudioPlayer

    class AudioPlayer(PySide.QtGui.QMainWindow, playerUI.Ui_MainWindow)
     |  Method resolution order:
     |      AudioPlayer
     |      PySide.QtGui.QMainWindow
     |      PySide.QtGui.QWidget
     |      PySide.QtCore.QObject
     |      PySide.QtGui.QPaintDevice
     |      Shiboken.Object
     |      playerUI.Ui_MainWindow
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, parent=None)
     |      # here we will make all connections with a GUI
     |  
     |  clear(self)
     |      # this method will clear a playlist when you click on Playlist-->Clear and
     |      # actionClear signal was emitted
     |  
     |  exit(self)
     |      # this method will close the application when button Exit was clicked or
     |      # you choose File-->Quit
     |  
     |  keyPressEvent(self, e)
     |  
     |  next(self)
     |      # this method will play next song from playlist random song,
     |      # if shuffle mode is on
     |      # this method will be called when button Next was clicked or
     |      # current song was finished (QMediaObject.finished signal was emitted)
     |  
     |  next_or_repeat(self)
     |      # this method will be called if repeat song mode is on and
     |      # current song was finished and QMediaObject.finished signal was emitted
     |  
     |  open(self)
     |      # this method will be called, when user clicks with mouse on File-->Open
     |      # (actio_Open signal was emitted)
     |      # after that you can see new dialog window from which you can choose
     |      # all music files for your playlist. With this method you can add
     |      # music files every time you want
     |  
     |  pause(self)
     |      # method that will pause song, if the song status is not "Paused"
     |      # this method will be called when you click on button Pause
     |  
     |  play(self)
     |      # method that will play song, if the song status is not "Playing"
     |      # this method will be called when you click on button Play
     |      # this method should be called every time when you want to play
     |      # current media object
     |  
     |  play_first(self)
     |      # method that will play first song in playlist
     |      # this method will be called when repeat playlist mode is on and
     |      # after current song finished signal was emitted() or user
     |      # clicks on button Next
     |  
     |  play_item(self, item)
     |      # method that will play double clicked song
     |      # user can choose song from playlist and when clicks twice on it, this
     |      # method will be called.
     |      # item is argument given by QListWidget.itemDoubleClicked signal
     |  
     |  play_last(self)
     |      # this method will play last song in playlist
     |  
     |  previous(self)
     |      # this method will start previous song in playlist
     |      # when button Previous was clicked
     |  
     |  random_song(self)
     |      # this method will be called if random song mode is on and
     |      # current song was finished (QMediaObject.finished signal was emitted) or
     |      # button Next was clicked
     |  
     |  remove(self)
     |      # this method will remove selected song from playlist
     |      # this method will be called when you pres Delete button on your keyboard
     |  
     |  search(self)
     |      # this method will be called when you choose Playlist-->Search
     |      # this method will filter all songs in playlist in which name
     |      # there is your input text
     |  
     |  shuffle_songs(self)
     |      # this method will shuffle my songs when actionShuffle signal was emitted
     |      # this method will be called when you click on Playlist-->Shuffle
     |  
     |  slider_value_change(self)
     |      # this method will called when you drag slider and play song from
     |      # the time which is equal to new slider value
     |  
     |  sort(self, code)
     |      # this method sort playlist by file(f), title(t), artist(a) and year(y)
     |      # this method will be called when you choose Playlist-->Sort by-->key
     |      # where key is one of Filename, Artist, Title or Year
     |  
     |  stop(self)
     |      # method will stop song, if the song status is not "Stopped"
     |      # this method will be called when you click on button Stop
     |  
     |  time_change(self, time)
     |      # this method move slider every time when QMediaObject.tick signal was
     |      # emitted
     |  
     |  total_time_change(self, time)
     |      # this method set range for slider, when totalTimeChanged signal was
     |      # emitted
FILE
	../player.py


## class Playlist
    playlist

    class Playlist(builtins.object)
     |  Static methods defined here:
     |  
     |  sort_by_artist(playlist)
     |      # this method will sort a playlist by artist/alphabetically
     |  
     |  sort_by_filename(playlist)
     |      # this method will sort a playlist by filename alphabetically
     |  
     |  sort_by_genre(playlist)
     |      # this method will sort a playlist by genre/alphabetically
     |  
     |  sort_by_title(playlist)
     |      # this method will sort a playlist by title/alphabetically
     |  
     |  sort_by_year(playlist)
     |      # this method will sort playlist by year
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FILE
    ../playlist.py

