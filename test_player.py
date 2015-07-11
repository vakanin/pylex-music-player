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

    def test_sort_by_filename(self):
        current_playlist = []
        for index in range(self.player.listWidget.count()):
            current_playlist.append(self.player.listWidget.item(index).text())
        self.player.actionFilename.triggered.emit()
        sorted_by_filename = Playlist.sort_by_filename(current_playlist)
        result = []
        for index in range(self.player.listWidget.count()):
            result.append(self.player.listWidget.item(index).text())
        self.assertEqual(result, sorted_by_filename)

    def test_sort_by_title(self):
        title_song_name = []
        for song_name, filename in self.player.full_paths.items():
            audio = ID3(filename)
            try:
                # in this way we can get title
                title = audio['TIT2'].text[0]
            except:
                title = ''
            title_song_name.append((song_name, title))
        self.player.actionTitle.triggered.emit()
        sorted_by_title = Playlist.sort_by_title(title_song_name)
        result_check = [song for song, _ in sorted_by_title]
        result = []
        for index in range(self.player.listWidget.count()):
            result.append(self.player.listWidget.item(index).text())
        self.assertEqual(result, result_check)

    def test_sort_by_genre(self):
        genre_song_name = []
        for song_name, filename in self.player.full_paths.items():
            audio = ID3(filename)
            try:
                # in this way we can get genre
                genre = audio['TCON'].text[0]
            except:
                genre = ''
            genre_song_name.append((song_name, genre))
        self.player.actionGenre.triggered.emit()
        sorted_by_genre = Playlist.sort_by_genre(genre_song_name)
        result_check = [song for song, _ in sorted_by_genre]
        result = []
        for index in range(self.player.listWidget.count()):
            result.append(self.player.listWidget.item(index).text())
        self.assertEqual(result, result_check)

    def test_sort_by_artist(self):
        artist_song_name = []
        for song_name, filename in self.player.full_paths.items():
            audio = ID3(filename)
            try:
                # in this way we can get artist
                artist = audio['TPE1'].text[0]
            except:
                artist = ''
            artist_song_name.append((song_name, artist))
        self.player.actionArtist.triggered.emit()
        sorted_by_artist = Playlist.sort_by_artist(artist_song_name)
        result_check = [song for song, _ in sorted_by_artist]
        result = []
        for index in range(self.player.listWidget.count()):
            result.append(self.player.listWidget.item(index).text())
        self.assertEqual(result, result_check)

    def test_sort_by_year(self):
        year_song_name = []
        for song_name, filename in self.player.full_paths.items():
            audio = ID3(filename)
            try:
                # in this way we can get year
                year = audio['TDRC'].text[0]
            except:
                year = ''
            year_song_name.append((song_name, year))
        self.player.actionYear.triggered.emit()
        sorted_by_year = Playlist.sort_by_year(year_song_name)
        result_check = [song for song, _ in sorted_by_year]
        result = []
        for index in range(self.player.listWidget.count()):
            result.append(self.player.listWidget.item(index).text())
        self.assertEqual(result, result_check)

    def test_shuffle_songs(self):
        items = []
        for index in range(self.player.listWidget.count()):
            items.append(self.player.listWidget.item(index).text())
        self.player.shuffle_songs()
        shuffeled_items = []
        for index in range(self.player.listWidget.count()):
            shuffeled_items.append(self.player.listWidget.item(index).text())
        self.assertNotEqual(items, shuffeled_items)

    def test_remove(self):
        item = self.player.listWidget.currentItem()
        item.setSelected(True)
        song_name = item.text()
        count_before_remove = self.player.listWidget.count()
        self.player.remove()
        count_after_remove = self.player.listWidget.count()
        self.assertNotIn(song_name, list(self.player.full_paths.keys()))
        self.assertEqual(count_before_remove, count_after_remove + 1)


class TestPlaylist(unittest.TestCase):

    def setUp(self):
        self.list_to_sort = [4, 2, 1, 8, 101, 29]
        self.list_of_tuples = [('w', 3), ('b', 1), ('k', 4), ('d', 2)]

    def test_sort_by_filename(self):
        sorted_list = Playlist.sort_by_filename(self.list_to_sort)
        self.assertEqual(sorted_list, [1, 2, 4, 8, 29, 101])

    def test_sort_by_title(self):
        sorted_list = Playlist.sort_by_title(self.list_of_tuples)
        self.assertEqual(sorted_list,
                         [('b', 1), ('d', 2), ('w', 3), ('k', 4)])

    def test_sort_by_artist(self):
        sorted_list = Playlist.sort_by_title(self.list_of_tuples)
        self.assertEqual(sorted_list,
                         [('b', 1), ('d', 2), ('w', 3), ('k', 4)])

    def test_sort_by_year(self):
        sorted_list = Playlist.sort_by_title(self.list_of_tuples)
        self.assertEqual(sorted_list,
                         [('b', 1), ('d', 2), ('w', 3), ('k', 4)])

    def test_sort_by_genre(self):
        sorted_list = Playlist.sort_by_title(self.list_of_tuples)
        self.assertEqual(sorted_list,
                         [('b', 1), ('d', 2), ('w', 3), ('k', 4)])

if __name__ == '__main__':
    app = PySide.QtGui.QApplication(sys.argv)
    window = AudioPlayer()
    unittest.main()
