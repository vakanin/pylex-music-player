import unittest
from player import *
import playerUI
from PyQt4 import *
from time import sleep
from copy import copy

class TestAudioPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.player = AudioPlayer()
#        song_name = '216. SWEDEN - Loreen - Euphoria'
#        filename = './music_files/216. SWEDEN - Loreen - Euphoria'
#        cls.player.audio_output = Phonon.AudioOutput(Phonon.MusicCategory)
#        Phonon.createPath(cls.player.media_obj, cls.player.audio_output)
#        cls.player.media_obj.setCurrentSource(Phonon.MediaSource(filename))
#        cls.player.media_obj.tick.connect(cls.player.time_change)
#        cls.player.media_obj.totalTimeChanged.connect(cls.player.total_time_change)
#        cls.player.volumeSlider.setAudioOutput(cls.player.audio_output)
        cls.player.open()

    def tearDown(self):
        self.player.randomCheckBox.setChecked(False)
        self.player.repeatCheckBox.setChecked(False)
        self.player.actionRepeat.setChecked(False)

    def test_play(self):
        self.player.play()
        self.assertEqual(self.player.media_state, 'Playing')

    def test_stop(self):
        self.player.play()
        self.player.stop()
        self.assertEqual(self.player.media_state, 'Stopped')

    def test_pause(self):
        self.player.pause()
        self.assertEqual(self.player.media_state, 'Paused')

    def test_next(self):
        current_index = self.player.listWidget.currentRow()
        next_song = self.player.listWidget.item(current_index + 1).text()
        self.player.next()
        next_song_result = self.player.listWidget.currentItem().text()
        self.assertEqual(next_song, next_song_result)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_previous(self):
        self.player.next()
        current_index = self.player.listWidget.currentRow()
        previous_song = self.player.listWidget.item(current_index - 1).text()
        self.player.previous()
        previous_song_result = self.player.listWidget.currentItem().text()
        self.assertEqual(previous_song, previous_song_result)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_repeat_song(self):
        self.player.repeatCheckBox.setChecked(True)
        current_song = self.player.listWidget.currentItem().text()
        self.player.media_obj.finished.emit()
        next_song = self.player.listWidget.currentItem().text()
        self.assertEqual(current_song, next_song)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_play_first(self):
        first_song = self.player.listWidget.item(0).text()
        self.player.play_first()
        current_song = self.player.listWidget.currentItem().text()
        self.assertEqual(first_song, current_song)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_play_last(self):
        last_index = self.player.listWidget.count() - 1
        last_song = self.player.listWidget.item(last_index).text()
        self.player.play_last()
        current_song = self.player.listWidget.currentItem().text()
        self.assertEqual(last_song, current_song)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_repeat_playlist(self):
        self.player.actionRepeat.setChecked(True)
        first_song = self.player.listWidget.item(0).text()
        self.player.play_last()
        self.player.next()
        current_song = self.player.listWidget.currentItem().text()
        current_index = self.player.listWidget.currentRow()
        self.assertEqual(current_song, first_song)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_play_first(self):
        first_song = self.player.listWidget.item(0).text()
        self.player.play_first()
        current_song = self.player.listWidget.currentItem().text()
        self.assertEqual(first_song, current_song)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_play_last(self):
        last_index = self.player.listWidget.count() - 1
        last_song = self.player.listWidget.item(last_index).text()
        self.player.play_last()
        current_song = self.player.listWidget.currentItem().text()
        self.assertEqual(last_song, current_song)
        self.assertEqual(self.player.media_state, 'Playing')

    def test_random_song(self):
        self.player.randomCheckBox.setChecked(True)
        current_index = self.player.listWidget.currentRow()
        next_index = current_index + 1
        prev_index = current_index - 1
        self.player.media_obj.finished.emit()
        self.player.next()
        self.player.next()
        self.player.next()
        playing_song_index = self.player.listWidget.currentRow()
        self.assertNotEqual(next_index, prev_index, playing_song_index)
        self.assertEqual(self.player.media_state, 'Playing')

    @unittest.skip("sorting test skipped")
    def test_sort(self):
        pass

    def test_shuffle_songs(self):
        items = []
        for index in range(self.player.listWidget.count()):
            items.append(self.player.listWidget.item(index).text())
        self.player.shuffle_songs()
        shuffeled_items = []
        for index in range(self.player.listWidget.count()):
            shuffeled_items.append(self.player.listWidget.item(index).text())
        self.assertNotEqual(items, shuffeled_items)

#    @unittest.skip
#    def test_scrobble(self):
#        pass
#
#
#class TestPlaylist(unittest.TestCase):
#
#    def test_sort_by_title(self):
#        pass
#
#    def test_sort_by_artist(self):
#        pass
#
#    def test_sort_by_album(self):
#        pass
#
#    def test_sort_by_year(self):
#        pass
#
#    def test_sort_by_genre(self):
#        pass
#
#    def test_shuffle(self):
#        pass
#
#
if __name__ == '__main__':
    app = PySide.QtGui.QApplication(sys.argv)
    window = AudioPlayer()
    unittest.main()
