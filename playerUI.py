# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player.ui'
#
# Created: Wed Jul  8 03:47:33 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 592)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.playButton = QtGui.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(320, 280, 99, 41))
        self.playButton.setObjectName("playButton")
        self.stopButton = QtGui.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(20, 240, 99, 41))
        self.stopButton.setObjectName("stopButton")
        self.exitButton = QtGui.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(20, 290, 99, 27))
        self.exitButton.setObjectName("exitButton")
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(140, 250, 471, 31))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.pictureLabel = QtGui.QLabel(self.centralwidget)
        self.pictureLabel.setGeometry(QtCore.QRect(30, 10, 581, 191))
        self.pictureLabel.setText("")
        self.pictureLabel.setPixmap(QtGui.QPixmap("pics/party.jpg"))
        self.pictureLabel.setScaledContents(True)
        self.pictureLabel.setObjectName("pictureLabel")
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 340, 581, 191))
        self.listWidget.setObjectName("listWidget")
        self.nowPlayingLabel = QtGui.QLabel(self.centralwidget)
        self.nowPlayingLabel.setGeometry(QtCore.QRect(140, 210, 471, 20))
        self.nowPlayingLabel.setText("")
        self.nowPlayingLabel.setObjectName("nowPlayingLabel")
        self.prevButton = QtGui.QPushButton(self.centralwidget)
        self.prevButton.setGeometry(QtCore.QRect(250, 280, 51, 41))
        self.prevButton.setObjectName("prevButton")
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(440, 280, 51, 41))
        self.nextButton.setObjectName("nextButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.action_Quit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.playButton.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.stopButton.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.prevButton.setText(QtGui.QApplication.translate("MainWindow", "<<", None, QtGui.QApplication.UnicodeUTF8))
        self.nextButton.setText(QtGui.QApplication.translate("MainWindow", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))

