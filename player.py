import sys
from PySide.QtCore import *
from PySide.QtGui import *
from playerUI import *

from PySide.phonon import Phonon


class AudioPlayer(Ui_MainWindow()):

    def __init__(self):
        self.SetupUi(self)
        self.media_obj = Phonon.MediaObject(self)
        self.current_time = 0

    # method that will play song, if the song status is not "playing"
    def play(self):
        if Phonon.State.PlayingState != self.media_obj.state():
            self.media_obj.play()

    # method that will pause song, if the song status is not "paused"
    def pause(self):
        if Phonon.State.PausedState != self.media_obj.state():
            self.media_obj.pause()

    # this method will play next song from playlist or maybe random song,
    # if shuffle mode is on
    def next(self):
        pass

    # this method will start previous song in playlist
    def previous(self):
        pass

    # repeat current song while repeat mode is on
    def repeat_song(self):
        pass

    # will play current playlist if repeat mode for playlist is active
    def repeat_playlist(self):
        pass

    # increase volume
    def volume_up(self):
        pass

    # decrease volume
    def volume_down(self):
        pass

    # this method will open a dialog window,
    # from which you can select .mp3 file to be added
    def add_in_playlist(self):
        pass

    # this method will remove selected song from playlist
    def remove_from_playlist(self):
        pass

    # this method will load new playlist
    def load_playlist(self):
        pass

    # I don't know exactly how to implement this method, but I suppose that
    # will be something conncected with Last.fm or maybe not :)
    def scrobble(self):
        pass

    # this method will close the application
    def exit(self):
        sys.exit()


class PlayList():

    def __init__(self):
        pass

    # this method will sort a playlist alphabetically
    def sort_by_title(self):
        pass

    # this method will sort a playlist by genre/alphabetically
    def sort_by_genre(self):
        pass

    # this method will sort a playlist by artist/alphabetically
    def sort_by_artist(self):
        pass

    # this method ala bala ... by year
    def sort_by_year(self):
        pass

    # ... by album
    def sort_by_album(self):
        pass

    # this method will shuffle a playlist
    def shuffle(self):
        pass
