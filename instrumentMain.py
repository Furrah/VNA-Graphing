from PyQt5 import QtGui , QtCore 
import sys # We need sys so that we can pass argv to QApplication
import pyqtgraph as pg
import InstrumentGraphingV3 # This file holds our MainWindow and all design related things
import qdarkstyle
import qdarkgraystyle
import numpy as np 
import os 
import time 

class IG(QtGui.QMainWindow, InstrumentGraphingV3.Ui_MainWindow):
	def __init__(self):

		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically

		self.Graph.setLogMode(x = True, y = False)
		self.Graph.showGrid(x=True, y=True, alpha=1)

		self.curve1 = self.Graph.plot(pen = pg.mkPen('y', width =1),name = 'yellow plot') 

		self.Graph2.setLogMode(x = True, y = False)
		self.Graph2.showGrid(x=True, y=True, alpha=1)
		self.curve2 = self.Graph2.plot(pen = pg.mkPen('c', width =1),name = 'blue plot')


		self.S11curves = [] 
		self.S21curves = []


		self.Graph.setLabel('bottom' ,'MHz')
		self.Graph2.setLabel('bottom' , 'MHz')

		self.Graph.setLabel('left','dB')
		self.Graph2.setLabel('left', 'dB')

		self.Graph.setLabel('top','S11')
		self.Graph2.setLabel('top', 'S21')

		self.butt_FileWrite.clicked.connect(self.selectFile)

		# self.colours = ['b', 'g', 'r', 'c', 'm', 'y', 'w']
		self.colours = ['y', 'c', 'm', 'b', 'g', 'r', 'w']

		self.i = 0

		self.pushButton.clicked.connect(self.removePlots)


	def selectFile(self):
		file = QtGui.QFileDialog.getOpenFileName()[0]

		if len(file) > 0:

			self.AddData(file)

	def removePlots(self):
		for curve in self.S11curves:
			self.Graph.removeItem(curve)

		for curve in self.S21curves:
			self.Graph2.removeItem(curve)	



	def AddData(self,file):



		A = self.get_data_LT(file)


		self.tempCurve = self.Graph.plot(pen = pg.mkPen(self.colours[self.i], width =1))
		self.tempCurve2 = self.Graph2.plot(pen = pg.mkPen(self.colours[self.i], width =1))

		self.tempCurve.setData(A[0]/1e6,A[1])
		self.tempCurve2.setData(A[0]/1e6,A[3])

		self.S11curves.append(self.tempCurve)
		self.S21curves.append(self.tempCurve2)

		self.i +=1

		cut_off = 0
		initial_gain = A[3][0]
		for i,value in enumerate(A[3]):

			# print(value)
			if ( value+initial_gain)  < -3:
				cut_off = i

				break	


		name = os.path.basename(file)

		self.label.setText(str(name))
		self.label_2.setText('-3dB cut off \n' +str(A[0][cut_off]/1e6)+ ' MHz')

		self.Graph2.scene().sigMouseMoved.connect(self.onMouseMoved)	


	def onMouseMoved(self, point):
		p = self.Graph2.plotItem.vb.mapSceneToView(point)
		self.statusBar().showMessage("{} MHz - {}".format(str(pow(10,float(p.x()))), p.y()))
		
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


	def mouseMoved(self,evt):
	  mousePoint = self.curve2.vb.mapSceneToView(evt[0])

	  self.label.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))



def main():
	app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
	#app.setStyleSheet(qdarkstyle.load_stylesheet(pyside = False))
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	# app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
	form = IG()                 # We set the form to be our ExampleApp (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main()  