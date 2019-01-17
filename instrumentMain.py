from PyQt5 import QtGui , QtCore 
import sys # We need sys so that we can pass argv to QApplication
import pyqtgraph as pg
import InstrumentGraphing # This file holds our MainWindow and all design related things
import qdarkstyle
import numpy as np 


class IG(QtGui.QMainWindow, InstrumentGraphing.Ui_MainWindow):
	def __init__(self):

		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically

		self.Graph.setLogMode(x = True, y = False)
		self.Graph.showGrid(x=True, y=True, alpha=1)
		self.curve1 = self.Graph.plot(pen = pg.mkPen('y', width =1),name = 'yellow plot') 

		self.Graph2.setLogMode(x = True, y = False)
		self.Graph2.showGrid(x=True, y=True, alpha=1)
		self.curve2 = self.Graph2.plot(pen = pg.mkPen('c', width =1),name = 'yellow plot') 

		self.butt_FileWrite.clicked.connect(self.selectFile)
 

	def selectFile(self):
		file = QtGui.QFileDialog.getOpenFileName()[0]
		self.Plot(file)



	def Plot(self,file):

		A = self.get_data_LT(file)

		self.curve1.setData(A[0]/1e6,A[1])
		self.curve2.setData(A[0]/1e6,A[3])

	def get_data_LT(self,file):
		with open(file,'r') as infile:	
			infile = infile.read()
			data = infile.split('\n')

			data = data[5:]

			D = [[] for i in range(9)]

			for eachline in data:

				if len(eachline) > 0:
					eachline = eachline.split('\t')

					for i in range(len(eachline)):
						D[i].append(float(eachline[i]))

			D = np.asarray(D)

			return D




def main():
	app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
	#app.setStyleSheet(qdarkstyle.load_stylesheet(pyside = False))
	# app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	#app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
	form = IG()                 # We set the form to be our ExampleApp (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main()  