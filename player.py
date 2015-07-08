import sys
import playerUI
import PySide
from PyQt4 import *
from functools import partial
from PySide.phonon import Phonon
from mutagen.id3 import ID3


class AudioPlayer(PySide.QtGui.QMainWindow, playerUI.Ui_MainWindow):

    def __init__(self, parent=None):
        super(AudioPlayer, self).__init__(parent)
        # full_paths contain full path name for each media
        self.full_paths = {}
        self.media_objects_info = {}
        self.setupUi(self)
        self.media_obj = Phonon.MediaObject(self)
        self.media_obj.aboutToFinish.connect(self.next)
        self.current_time = 0
        self.action_Open.triggered.connect(self.open)
        self.action_Quit.triggered.connect(self.exit)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setEnabled(False)
        self.horizontalSlider.sliderReleased.connect(self.slider_value_change)
        self.playButton.clicked.connect(self.play)
        self.playButton.setText('Play')
        self.playButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stop)
        self.stopButton.setEnabled(False)
        self.exitButton.clicked.connect(self.exit)
        self.exitButton.setEnabled(True)
        self.nextButton.clicked.connect(self.next)
        self.nextButton.setEnabled(False)
        self.prevButton.clicked.connect(self.previous)
        self.prevButton.setEnabled(False)
        self.listWidget.itemDoubleClicked.connect(self.play_item)
        self.volumeSlider = Phonon.VolumeSlider(self)
        self.volumeSlider.setGeometry(PySide.QtCore.QRect(520, 310, 91, 29))
        self.volumeSlider.setOrientation(PySide.QtCore.Qt.Horizontal)
        self.actionFilename.triggered.connect(partial(self.sort, 'f'))
        self.actionTitle.triggered.connect(partial(self.sort, 't'))
        self.actionArtist.triggered.connect(partial(self.sort, 'a'))
        self.actionYear.triggered.connect(partial(self.sort, 'y'))
        self.actionGenre.triggered.connect(partial(self.sort, 'g'))

    def open(self):
        self.actionTitle.setChecked(False)
        self.actionArtist.setChecked(False)
        self.actionYear.setChecked(False)
        self.actionGenre.setChecked(False)
        dialog = PySide.QtGui.QFileDialog()
        dialog.setViewMode(PySide.QtGui.QFileDialog.Detail)
        filenames = dialog.getOpenFileNames(self,
                                            'Open audio file',
                                            '/home/alex/Music',
                                            "Audio Files (*.mp3 *.wav *.ogg)")[0]

        song_names = []
        for filename in filenames:
            song_name = filename.split('/')[-1]
            song_names.append(song_name)            # this line will be removed
            self.listWidget.addItem(song_name)
            self.listWidget.show()
            self.full_paths[song_name] = filename
        self.listWidget.setCurrentRow(0)
        filename = filenames[0]
        song_name = filename.split('/')[-1]
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.media_obj, self.audio_output)
        self.media_obj.setCurrentSource(Phonon.MediaSource(filename))
        self.media_obj.tick.connect(self.time_change)
        self.media_obj.totalTimeChanged.connect(self.total_time_change)
        self.volumeSlider.setAudioOutput(self.audio_output)
        self.nowPlayingLabel.setText(song_name)
        self.media_obj.play()
        self.stopButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.playButton.setText("Pause")
        self.horizontalSlider.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.prevButton.setEnabled(True)

    # method that will play double clicked song
    def play_item(self, item):
        song_name = item.text()
        filename = self.full_paths[song_name]
        self.media_obj.setCurrentSource(Phonon.MediaSource(filename))
        self.media_obj.tick.connect(self.time_change)
        self.media_obj.totalTimeChanged.connect(self.total_time_change)
        self.nowPlayingLabel.setText(song_name)
        self.media_obj.play()

    # method that will play song, if the song status is not "playing"
    def play(self):
        if Phonon.State.PlayingState != self.media_obj.state():
            self.media_obj.play()
            self.playButton.setText('Pause')
        else:
            self.pause()

    # method that will pause song, if the song status is not "paused"
    def pause(self):
        if Phonon.State.PausedState != self.media_obj.state():
            self.media_obj.pause()
            self.playButton.setText('Play')

    # stop the song
    def stop(self):
        if Phonon.State.StoppedState != self.media_obj.state():
            self.media_obj.stop()
            self.current_time = 0
            self.playButton.setText('Play')

    def time_change(self, time):
        if not self.horizontalSlider.isSliderDown():
            self.horizontalSlider.setValue(time)

    def total_time_change(self, time):
        self.horizontalSlider.setRange(0, time)

    def slider_value_change(self):
        value = self.horizontalSlider.value()
        self.media_obj.seek(value)

    # this method will play next song from playlist or maybe random song,
    # if shuffle mode is on
    def next(self):
        current_row = self.listWidget.currentRow()
        if current_row == self.listWidget.count() - 1:
            self.stop()
        else:
            self.listWidget.setCurrentRow(current_row + 1)
            next_song_name = self.listWidget.item(current_row + 1).text()
            next_filename = self.full_paths[next_song_name]
            self.media_obj.setCurrentSource(Phonon.MediaSource(next_filename))
            self.media_obj.tick.connect(self.time_change)
            self.media_obj.totalTimeChanged.connect(self.total_time_change)
            self.nowPlayingLabel.setText(next_song_name)
            self.play()

    # this method will start previous song in playlist
    def previous(self):
        current_row = self.listWidget.currentRow()
        if current_row <= 0:
            self.stop()
            self.play()
        else:
            self.listWidget.setCurrentRow(current_row - 1)
            prev_song_name = self.listWidget.item(current_row - 1).text()
            prev_filename = self.full_paths[prev_song_name]
            self.media_obj.setCurrentSource(Phonon.MediaSource(prev_filename))
            self.media_obj.tick.connect(self.time_change)
            self.media_obj.totalTimeChanged.connect(self.total_time_change)
            self.nowPlayingLabel.setText(prev_song_name)
            self.play()

    # this method sort our playlist by file(f), title(t) and artist('a)
    def sort(self, code):
        if code == 'f':
            self.listWidget.sortItems()
            self.listWidget.show()
            self.actionTitle.setChecked(False)
            self.actionArtist.setChecked(False)
            self.actionYear.setChecked(False)
            self.actionGenre.setChecked(False)
        elif code == 't':
            title_song_name = []
            for song_name, filename in self.full_paths.items():
                audio = ID3(filename)
                try:
                    # in this way we can get title
                    title = audio['TIT2'].text[0]
                except:
                    title = ''
                title_song_name.append((song_name, title))
            sorted_title_song_name = Playlist.sort_by_title(title_song_name)
            songs_sorted_by_title = [song for song, title in
                                     sorted_title_song_name]
            self.listWidget.clear()
            self.listWidget.addItems(songs_sorted_by_title)
            self.listWidget.show()
            self.actionFilename.setChecked(False)
            self.actionArtist.setChecked(False)
            self.actionYear.setChecked(False)
            self.actionGenre.setChecked(False)
        elif code == 'a':
            artist_song_name = []
            for song_name, filename in self.full_paths.items():
                audio = ID3(filename)
                # in this way we can get artist name
                try:
                    artist = audio['TPE1'].text[0]
                except:
                    artist = ''
                artist_song_name.append((song_name, artist))
            sorted_artist_song_name = \
                Playlist.sort_by_artist(artist_song_name)
            songs_sorted_by_artist = [song for song, _ in
                                      sorted_artist_song_name]
            self.listWidget.clear()
            self.listWidget.addItems(songs_sorted_by_artist)
            self.listWidget.show()
            self.actionFilename.setChecked(False)
            self.actionTitle.setChecked(False)
            self.actionYear.setChecked(False)
            self.actionGenre.setChecked(False)
        elif code == 'y':
            year_song_name = []
            for song_name, filename in self.full_paths.items():
                audio = ID3(filename)
                # in this way we can get released year
                try:
                    year = audio['TDRC'].text[0]
                except:
                    year = '0'
                year_song_name.append((song_name, year))
            sorted_year_song_name = Playlist.sort_by_year(year_song_name)
            songs_sorted_by_year = [song for song, _ in
                                    sorted_year_song_name]
            self.listWidget.clear()
            self.listWidget.addItems(songs_sorted_by_year)
            self.listWidget.show()
            self.actionFilename.setChecked(False)
            self.actionTitle.setChecked(False)
            self.actionArtist.setChecked(False)
            self.actionGenre.setChecked(False)
        elif code == 'g':
            genre_song_name = []
            for song_name, filename in self.full_paths.items():
                audio = ID3(filename)
                try:
                    # in this way we can get genre
                    genre = audio['TCON'].text[0]
                except:
                    genre = ''
                genre_song_name.append((song_name, genre))
            sorted_genre_song_name = Playlist.sort_by_genre(genre_song_name)
            songs_sorted_by_genre = [song for song, _ in
                                     sorted_genre_song_name]
            self.listWidget.clear()
            self.listWidget.addItems(songs_sorted_by_genre)
            self.listWidget.show()
            self.actionFilename.setChecked(False)
            self.actionTitle.setChecked(False)
            self.actionArtist.setChecked(False)
            self.actionYear.setChecked(False)

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
    # will be something connected with Last.fm or maybe not :)
    def scrobble(self):
        pass

    # this method will close the application
    def exit(self):
        sys.exit()


class Playlist():

    # this method will sort a playlist by filename alphabetically
    @staticmethod
    def sort_by_filename(playlist):
        return sorted(playlist)

    # this method will sort a playlist by title/alphabetically
    @staticmethod
    def sort_by_title(playlist):
        return sorted(playlist, key=lambda tup: tup[1])

    # this method will sort a playlist by genre/alphabetically
    @staticmethod
    def sort_by_genre(playlist):
        return sorted(playlist, key=lambda tup: tup[1])

    # this method will sort a playlist by artist/alphabetically
    @staticmethod
    def sort_by_artist(playlist):
        return sorted(playlist, key=lambda tup: tup[1])

    # this method will sort playlist by year
    @staticmethod
    def sort_by_year(playlist):
        try:
            return sorted(playlist, key=lambda tup: tup[1])
        except:
            return playlist

    # this method will shuffle a playlist
    def shuffle(self):
        pass

    # this method will show current time of the song
    # and will update diagram line
    def time_change(self):
        pass

if __name__ == "__main__":
    app = PySide.QtGui.QApplication(sys.argv)
    window = AudioPlayer()
    window.show()
    sys.exit(app.exec_())
