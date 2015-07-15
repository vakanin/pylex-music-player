import playerUI
import PySide
from PyQt4 import *
from PySide.phonon import Phonon
from functools import partial


class PlayerGui(PySide.QtGui.QMainWindow, playerUI.Ui_MainWindow):

    def __init__(self, parent=None):
        super(PlayerGui, self).__init__(parent)
        self.setupUi(self)
        self.media_obj = Phonon.MediaObject(self)
        self.media_obj.finished.connect(self.next_or_repeat)
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

    def open_modifications(self):
        self.actionTitle.setChecked(False)
        self.actionArtist.setChecked(False)
        self.actionYear.setChecked(False)
        self.actionGenre.setChecked(False)
        self.stopButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.playButton.setText("Pause")
        self.horizontalSlider.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.prevButton.setEnabled(True)
        self.repeatCheckBox.setEnabled(True)
        self.randomCheckBox.setEnabled(True)

    def play_button_pause(self):
        self.playButton.setText("Pause")

    def play_button_play(self):
        self.playButton.setText("Play")

    def get_now_playing_label(self):
        return self.nowPlayingLabel.text()

    def set_now_playing_label(self, text):
        self.nowPlayingLabel.setText(text)

    def set_time_label(self, time):
        self.timeLabel.setText(time)

    def set_total_time_label(self, time):
        self.totalTimeLabel.setText(time)

    def set_horizontal_slider_value(self, value):
        self.horizontalSlider.setValue(value)

    def set_horizontal_slider_range(self, min_, max_):
        self.horizontalSlider.setRange(min_, max_)

    def get_horizontal_slider_value(self):
        return self.horizontalSlider.value()

    def sort_filename_modifications(self):
        self.actionTitle.setChecked(False)
        self.actionArtist.setChecked(False)
        self.actionYear.setChecked(False)
        self.actionGenre.setChecked(False)

    def sort_title_modifications(self):
        self.actionFilename.setChecked(False)
        self.actionArtist.setChecked(False)
        self.actionYear.setChecked(False)
        self.actionGenre.setChecked(False)

    def sort_artist_modifications(self):
        self.actionFilename.setChecked(False)
        self.actionTitle.setChecked(False)
        self.actionYear.setChecked(False)
        self.actionGenre.setChecked(False)

    def sort_year_modifications(self):
        self.actionFilename.setChecked(False)
        self.actionTitle.setChecked(False)
        self.actionArtist.setChecked(False)
        self.actionGenre.setChecked(False)

    def sort_genre_modifications(self):
        self.actionFilename.setChecked(False)
        self.actionTitle.setChecked(False)
        self.actionArtist.setChecked(False)
        self.actionYear.setChecked(False)

    def read_modifications(self):
        self.stopButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.horizontalSlider.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.prevButton.setEnabled(True)
        self.repeatCheckBox.setEnabled(True)
        self.randomCheckBox.setEnabled(True)

