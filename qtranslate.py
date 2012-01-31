#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
from PyQt4 import QtCore, QtGui
from xml.dom.minidom import parseString
from mainwindow import Ui_MainWindow
import re

BING_APP_ID = 'F6064743FC4157648662DCC48129DFB34911A549'
ABOUT_TEXT = '''
QTranslate is a simple Translation tools written in Python and Qt4 binding for Python, PyQt4.\n\nThis tool uses BING (Microsoft) Translation API to provide translation service.\n\nInternet connection is needed to run translation using this software.\n\nCopyright 2011 - Eka Putra\nEmail : ekaputra@balitechy.com\nWebsite : http://balitechy.com
'''

class QtranslateThread(QtCore.QThread):

      processDone = QtCore.pyqtSignal(str)
      isTranslating = QtCore.pyqtSignal(bool)
      appId = ''
      langFrom = ''
      langTo = ''
      theText = ''


      def run(self):
            self.isTranslating.emit(True)
            data = urllib.urlencode({'appId':self.appId,'from':self.langFrom, 'to':self.langTo,'text':self.theText,'contentType':'text/plain'})
            url = 'http://api.microsofttranslator.com/v2/Http.svc/Translate?'
            response = urllib.urlopen(url+data)
            result = response.read()
            response.close()

            filtered = re.search('<.*>(.*)</.*>', result)
            final_result = filtered.groups()[0]

            self.processDone.emit(final_result)
            self.isTranslating.emit(False)

class QTranslator(QtGui.QMainWindow):
      def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            self.thread = QtranslateThread()
            self.thread.processDone.connect(self.showTranslatedText)
            self.thread.isTranslating.connect(self.setStatus)


            QtCore.QObject.connect(self.ui.actionTranslate, QtCore.SIGNAL("activated()"), self.Translate)
            QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("activated()"), self.About)

      def About(self):
            global ABOUT_TEXT
            QtGui.QMessageBox.information(self, 'About QTranslate',ABOUT_TEXT, QtGui.QMessageBox.Ok)

      def Translate(self):
            global BING_APP_ID
            textOriginal = self.ui.txtOriginal.toPlainText()
            if not textOriginal:
                  QtGui.QMessageBox.warning(self, 'Hey dude!','Please provide me some text to translate...', QtGui.QMessageBox.Ok)
                  return False

            self.thread.appId = BING_APP_ID
            self.thread.theText = textOriginal
            self.thread.langFrom = str(self.ui.cbFrom.currentText())
            self.thread.langTo = str(self.ui.cbTo.currentText())

            self.thread.start()

      def showTranslatedText(self, string):
            self.ui.txtResult.setText(QtCore.QString(string))

      def setStatus(self, status):
            if status:
                  self.ui.lblStatus.setText('Loading...')
            else:
                  self.ui.lblStatus.setText('Ready...')


if __name__ == '__main__':
      app = QtGui.QApplication(sys.argv)
      qts = QTranslator()
      qts.show()
      sys.exit(app.exec_())

