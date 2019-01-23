from PyQt5 import QtGui , QtCore 
import sys # We need sys so that we can pass argv to QApplication
import pyqtgraph as pg
import InstrumentGraphingV2 # This file holds our MainWindow and all design related things
import qdarkstyle
import qdarkgraystyle
import numpy as np 
import os 

class IG(QtGui.QMainWindow, InstrumentGraphingV2.Ui_MainWindow):
	def __init__(self):

		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically

		self.Graph.setLogMode(x = True, y = False)
		self.Graph.showGrid(x=True, y=True, alpha=1)

		self.curve1 = self.Graph.plot(pen = pg.mkPen('y', width =1),name = 'yellow plot') 

		self.Graph2.setLogMode(x = True, y = False)
		self.Graph2.showGrid(x=True, y=True, alpha=1)
		self.curve2 = self.Graph2.plot(pen = pg.mkPen('c', width =1),name = 'yellow plot')



		self.Graph.setLabel('bottom' ,'MHz')
		self.Graph2.setLabel('bottom' , 'MHz')

		self.Graph.setLabel('left','dB')
		self.Graph2.setLabel('left', 'dB')

		self.Graph.setLabel('top','S11')
		self.Graph2.setLabel('top', 'S21')

		self.butt_FileWrite.clicked.connect(self.selectFile)

		# self.timer = QtCore.QTimer()
		# self.timer.timeout.connect(self.Update)
		
		# self.Trigger = False
		# if self.Trigger == True:
		# 	self.timer.start(100) 




	def selectFile(self):
		file = QtGui.QFileDialog.getOpenFileName()[0]
		self.Plot(file)



	def Plot(self,file):

		A = self.get_data_LT(file)

		self.curve1.setData(A[0]/1e6,A[1])
		self.curve2.setData(A[0]/1e6,A[3])

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



		self.curve2.scene().sigMouseMoved.connect(self.onMouseMoved)
		# self.Trigger = True
		# pg.SignalProxy(self.curve2.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

		# while True:
		# 	pg.QtGui.QApplication.processEvents()
		# print(proxy)

	# def Update(self):

	# 	proxy = pg.SignalProxy(self.Graph2.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

	# 	print(proxy)	
	def onMouseMoved(self, point):
		p = self.Graph2.plotItem.vb.mapSceneToView(point)
		self.statusBar().showMessage("{} MHz - {}".format(str(pow(10,float(p.x()))), p.y()))
		# self.statusBar().showMessage("{}-{}".format(p.x(), p.y()))
		
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