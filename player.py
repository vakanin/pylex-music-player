import sys
import playerUI
import PySide
from PyQt4 import *
from functools import partial
from PySide.phonon import Phonon
from mutagen.id3 import ID3
from random import randint, choice
from playlist import *


class AudioPlayer(PySide.QtGui.QMainWindow, playerUI.Ui_MainWindow):

    # here we will make all connections with a GUI
    def __init__(self, parent=None):
        super(AudioPlayer, self).__init__(parent)
        # full_paths contain full path name for each media
        self.full_paths = {}
        self.media_objects_info = {}
        self.setupUi(self)
        self.media_obj = Phonon.MediaObject(self)
        self.media_obj.finished.connect(self.next_or_repeat)
        self.media_state = 'Unknown'
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
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.volumeSlider.setAudioOutput(self.audio_output)
 
        self.actionFilename.triggered.connect(partial(self.sort, 'f'))
        self.actionTitle.triggered.connect(partial(self.sort, 't'))
        self.actionArtist.triggered.connect(partial(self.sort, 'a'))
        self.actionYear.triggered.connect(partial(self.sort, 'y'))
        self.actionGenre.triggered.connect(partial(self.sort, 'g'))
        self.actionClear.triggered.connect(self.clear)
        self.actionShuffle.triggered.connect(self.shuffle_songs)
        self.actionSearch.triggered.connect(self.search)
        self.action_search_emitted = False      # True if search mode is ON
        self.setAcceptDrops(True)

    def keyPressEvent(self, e):
        if e.key() == PySide.QtCore.Qt.Key_Delete:
            self.remove()

    # this method will be called, when user clicks with mouse on File-->Open
    # (actio_Open signal was emitted)
    # after that you can see new dialog window from which you can choose
    # all music files for your playlist. With this method you can add
    # music files every time you want
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
        curr_index = self.listWidget.count()
        for filename in filenames:
            song_name = filename.split('/')[-1]
            song_names.append(song_name)            # this line will be removed
            self.listWidget.addItem(song_name)
            self.listWidget.show()
            self.full_paths[song_name] = filename
        self.listWidget.setCurrentRow(curr_index)
        filename = filenames[0]
        song_name = filename.split('/')[-1]
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.media_obj.setCurrentSource(Phonon.MediaSource(filename))
        self.media_obj.tick.connect(self.time_change)
        self.media_obj.totalTimeChanged.connect(self.total_time_change)
        self.nowPlayingLabel.setText(song_name)
        self.media_obj.play()
        self.media_state = 'Playing'
        self.stopButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.playButton.setText("Pause")
        self.horizontalSlider.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.prevButton.setEnabled(True)
        self.repeatCheckBox.setEnabled(True)
        self.randomCheckBox.setEnabled(True)

    # method that will play first song in playlist
    # this method will be called when repeat playlist mode is on and
    # after current song finished signal was emitted() or user
    # clicks on button Next
    def play_first(self):
        song_name = self.listWidget.item(0).text()
        filename = self.full_paths[song_name]
        Phonon.createPath(self.media_obj, self.audio_output)
        self.media_obj.setCurrentSource(Phonon.MediaSource(filename))
        self.media_obj.tick.connect(self.time_change)
        self.media_obj.totalTimeChanged.connect(self.total_time_change)
        self.nowPlayingLabel.setText(song_name)
        self.listWidget.setCurrentRow(0)
        self.play()

    # this method will play last song in playlist
    def play_last(self):
        last_index = self.listWidget.count() - 1
        song_name = self.listWidget.item(last_index).text()
        filename = self.full_paths[song_name]
        Phonon.createPath(self.media_obj, self.audio_output)
        self.media_obj.setCurrentSource(Phonon.MediaSource(filename))
        self.media_obj.tick.connect(self.time_change)
        self.media_obj.totalTimeChanged.connect(self.total_time_change)
        self.nowPlayingLabel.setText(song_name)
        self.listWidget.setCurrentRow(last_index)
        self.play()

    # method that will play double clicked song
    # user can choose song from playlist and when clicks twice on it, this
    # method will be called.
    # item is argument given by QListWidget.itemDoubleClicked signal
    def play_item(self, item):
        song_name = item.text()
        filename = self.full_paths[song_name]
        self.media_obj.setCurrentSource(Phonon.MediaSource(filename))
        self.media_obj.tick.connect(self.time_change)
        self.media_obj.totalTimeChanged.connect(self.total_time_change)
        self.nowPlayingLabel.setText(song_name)
        self.play()
        if self.action_search_emitted is True:
            # this is because search method
            current_playlist = [song for song, _ in self.full_paths.items()]
            current_song = self.nowPlayingLabel.text()
            current_playlist = sorted(current_playlist)
            for index, song in enumerate(current_playlist):
                if song == current_song:
                    current_row = index
            self.listWidget.clear()
            self.listWidget.addItems(current_playlist)
            self.listWidget.setCurrentRow(current_row)
            self.action_search_emitted = False

    # method that will play song, if the song status is not "Playing"
    # this method will be called when you click on button Play
    # this method should be called every time when you want to play
    # current media object
    def play(self):
        if Phonon.State.PlayingState != self.media_obj.state():
            self.media_obj.play()
            self.media_state = 'Playing'
            self.playButton.setText('Pause')
        else:
            self.pause()
            self.media_state = 'Paused'

    # method that will pause song, if the song status is not "Paused"
    # this method will be called when you click on button Pause
    def pause(self):
        if Phonon.State.PausedState != self.media_obj.state():
            self.media_obj.pause()
            self.media_state = 'Paused'
            self.playButton.setText('Play')

    # method will stop song, if the song status is not "Stopped"
    # this method will be called when you click on button Stop
    def stop(self):
        if Phonon.State.StoppedState != self.media_obj.state():
            self.media_obj.stop()
            self.current_time = 0
            self.playButton.setText('Play')
        self.media_state = 'Stopped'

    # this method move slider every time when QMediaObject.tick signal was
    # emitted
    def time_change(self, time):
        if not self.horizontalSlider.isSliderDown():
            self.horizontalSlider.setValue(time)
        s = time / 1000
        m, s = divmod(s, 60)
        min_ = str(int(m))
        sec = str(int(s))
        if len(sec) < 2:
            sec = '0' + sec
        self.timeLabel.setText(min_ + ':' + sec)

    # this method set range for slider, when totalTimeChanged signal was
    # emitted
    def total_time_change(self, time):
        self.horizontalSlider.setRange(0, time)
        s = time / 1000
        m, s = divmod(s, 60)
        min_ = str(int(m))
        sec = str(int(s))
        if len(sec) < 2:
            sec = '0' + sec
        if self.media_state == 'Stopped':
            self.totalTimeLabel.setText('0:00')
        else:
            self.totalTimeLabel.setText(min_ + ':' + sec)

    # this method will called when you drag slider and play song from
    # the time which is equal to new slider value
    def slider_value_change(self):
        value = self.horizontalSlider.value()
        self.media_obj.seek(value)

    # this method will be called if repeat song mode is on and
    # current song was finished and QMediaObject.finished signal was emitted
    def next_or_repeat(self):
        if self.repeatCheckBox.isChecked():
            self.play()
        else:
            self.next()

    # this method will be called if random song mode is on and
    # current song was finished (QMediaObject.finished signal was emitted) or
    # button Next was clicked
    def random_song(self):
        row_index = randint(0, self.listWidget.count() - 1)
        self.listWidget.setCurrentRow(row_index)
        song_name = self.listWidget.item(row_index).text()
        filename = self.full_paths[song_name]
        self.media_obj.setCurrentSource(Phonon.MediaSource(filename))
        self.media_obj.tick.connect(self.time_change)
        self.media_obj.totalTimeChanged.connect(self.total_time_change)
        self.nowPlayingLabel.setText(song_name)
        self.play()

    # this method will play next song from playlist random song,
    # if shuffle mode is on
    # this method will be called when button Next was clicked or
    # current song was finished (QMediaObject.finished signal was emitted)
    def next(self):
        if self.randomCheckBox.isChecked():
            return self.random_song()
        current_row = self.listWidget.currentRow()
        if current_row >= self.listWidget.count() - 1:
            if self.actionRepeat.isChecked():
                self.play_first()
            else:
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
    # when button Previous was clicked
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

    # this method sort playlist by file(f), title(t), artist(a) and year(y)
    # this method will be called when you choose Playlist-->Sort by-->key
    # where key is one of Filename, Artist, Title or Year
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
            songs_sorted_by_title = [song for song, _ in
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

    # this method will shuffle my songs when actionShuffle signal was emitted
    # this method will be called when you click on Playlist-->Shuffle
    def shuffle_songs(self):
        all_songs = []
        for index in range(self.listWidget.count()):
            all_songs.append(self.listWidget.item(index).text())
        self.listWidget.clear()
        for index in range(len(all_songs)):
            song = choice(all_songs)
            self.listWidget.addItem(song)
            all_songs.remove(song)
        self.listWidget.show()

    # this method will be called when you choose Playlist-->Search
    # this method will filter all songs in playlist in which name
    # there is your input text
    def search(self):
        dialog = PySide.QtGui.QInputDialog()
        text, ok = dialog.getText(self, 'Search dialog', 'Enter song name:')
        text = text.lower()
        if ok:
            current_playlist = []
            for index in range(self.listWidget.count()):
                current_playlist.append(self.listWidget.item(index).text())
            filtered_playlist = []
            for song in current_playlist:
                if text in song.lower():
                    filtered_playlist.append(song)
            if filtered_playlist:
                self.listWidget.clear()
                self.listWidget.addItems(filtered_playlist)
                self.listWidget.show()
                self.action_search_emitted = True

    # this method will remove selected song from playlist
    # this method will be called when you pres Delete button on your keyboard
    def remove(self):
        if self.action_search_emitted is False:
            current_playlist = []
            for index in range(self.listWidget.count()):
                current_playlist.append(self.listWidget.item(index).text())
            all_selected_items = self.listWidget.selectedItems()
            for song in all_selected_items:
                song_name = song.text()
                del self.full_paths[song_name]
                current_playlist.remove(song_name)
            self.listWidget.clear()
            self.listWidget.addItems(current_playlist)
            self.listWidget.show()
        else:
            all_selected_items = self.listWidget.selectedItems()
            for song in all_selected_items:
                song_name = song.text()
                del self.full_paths[song_name]
            playlist = [song for song, _ in self.full_paths.items()]
            self.listWidget.clear()
            self.listWidget.addItems(playlist)
            self.listWidget.show()

    # this method will clear a playlist when you click on Playlist-->Clear and
    # actionClear signal was emitted
    def clear(self):
        self.full_paths = {}
        self.listWidget.clear()
        self.listWidget.show()

    # this method will close the application when button Exit was clicked or
    # you choose File-->Quit
    def exit(self):
        sys.exit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(PySide.QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(PySide.QtCore.Qt.CopyAction)
            event.accept()
            filenames = []
            for url in event.mimeData().urls():
                filenames.append(str(url.toLocalFile()))
            self.read(filenames)
        else:
            event.ignore()

    def read(self, filenames):
        song_names = []
        for filename in filenames:
            song_name = filename.split('/')[-1]
            song_names.append(song_name)
            self.full_paths[song_name] = filename
        self.listWidget.addItems(song_names)
        self.listWidget.show()
        self.stopButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.horizontalSlider.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.prevButton.setEnabled(True)
        self.repeatCheckBox.setEnabled(True)
        self.randomCheckBox.setEnabled(True)
        self.play_first()

if __name__ == "__main__":
    app = PySide.QtGui.QApplication(sys.argv)
    window = AudioPlayer()
    window.show()
    sys.exit(app.exec_())
