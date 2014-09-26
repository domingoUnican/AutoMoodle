# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interfaz.ui'
#
# Created: Mon Sep 08 02:44:18 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(431, 226)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.BDescargar = QtGui.QPushButton(self.centralwidget)
        self.BDescargar.setGeometry(QtCore.QRect(20, 90, 111, 23))
        self.BDescargar.setObjectName(_fromUtf8("BDescargar"))
        self.BEntregas = QtGui.QPushButton(self.centralwidget)
        self.BEntregas.setGeometry(QtCore.QRect(20, 120, 111, 23))
        self.BEntregas.setObjectName(_fromUtf8("BEntregas"))
        self.BCancelar = QtGui.QPushButton(self.centralwidget)
        self.BCancelar.setGeometry(QtCore.QRect(20, 150, 111, 23))
        self.BCancelar.setObjectName(_fromUtf8("BCancelar"))
        self.CBAsignaturas = QtGui.QComboBox(self.centralwidget)
        self.CBAsignaturas.setGeometry(QtCore.QRect(130, 20, 281, 22))
        self.CBAsignaturas.setObjectName(_fromUtf8("CBAsignaturas"))
        self.CBTareas = QtGui.QComboBox(self.centralwidget)
        self.CBTareas.setGeometry(QtCore.QRect(130, 50, 281, 22))
        self.CBTareas.setObjectName(_fromUtf8("CBTareas"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 50, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.LUsuario = QtGui.QLineEdit(self.centralwidget)
        self.LUsuario.setGeometry(QtCore.QRect(240, 150, 181, 20))
        self.LUsuario.setText(_fromUtf8(""))
        self.LUsuario.setObjectName(_fromUtf8("LUsuario"))
        self.LPass = QtGui.QLineEdit(self.centralwidget)
        self.LPass.setGeometry(QtCore.QRect(240, 180, 181, 20))
        self.LPass.setText(_fromUtf8(""))
        self.LPass.setEchoMode(QtGui.QLineEdit.Password)
        self.LPass.setObjectName(_fromUtf8("LPass"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 150, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(165, 180, 61, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 210, 431, 16))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(150, 100, 121, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.LDir = QtGui.QLineEdit(self.centralwidget)
        self.LDir.setGeometry(QtCore.QRect(280, 100, 141, 20))
        self.LDir.setObjectName(_fromUtf8("LDir"))
        self.BAcceder = QtGui.QPushButton(self.centralwidget)
        self.BAcceder.setGeometry(QtCore.QRect(20, 180, 111, 23))
        self.BAcceder.setObjectName(_fromUtf8("BAcceder"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.BDescargar.setText(_translate("MainWindow", "Descargar Entregas", None))
        self.BEntregas.setText(_translate("MainWindow", "Evaluar Entregas", None))
        self.BCancelar.setText(_translate("MainWindow", "Cancelar", None))
        self.label.setText(_translate("MainWindow", "Asignaturas:", None))
        self.label_2.setText(_translate("MainWindow", "Tareas:", None))
        self.label_3.setText(_translate("MainWindow", "Usuario:", None))
        self.label_4.setText(_translate("MainWindow", "Contraseña:", None))
        self.label_5.setText(_translate("MainWindow", "Directorio Evaluaciones:", None))
        self.BAcceder.setText(_translate("MainWindow", "Acceder", None))

