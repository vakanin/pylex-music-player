import unittest
from player import *
import playerUI
from PyQt4 import *
from time import sleep

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
        current_index = self.player.listWidget.currentRow()
        previous_song = self.player.listWidget.item(current_index - 1).text()
        self.player.previous()
        previous_song_result = self.player.listWidget.currentItem().text()
        self.assertEqual(previous_song, previous_song_result)
        self.assertEqual(self.player.media_state, 'Playing')

#    @unittest.skip
#    def test_repeat_song(self):
#        pass
#
#    @unittest.skip
#    def test_repeat_playlist(self):
#        pass
#
#    @unittest.skip
#    def test_volume_up(self):
#        pass
#
#    @unittest.skip
#    def test_volume_down(self):
#        pass
#
#    @unittest.skip
#    def test_add_in_playlist(self):
#        pass
#
#    @unittest.skip
#    def test_remove_from_playlist(self):
#        pass
#
#    @unittest.skip
#    def test_load_playlist(self):
#        pass
#
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
