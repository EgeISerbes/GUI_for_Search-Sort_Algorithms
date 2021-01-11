
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import time




class MainWindow(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.storedList = []
        self.unsortedList = []
        self.isSearch = False
        self.errorDict = {"ValueNotEnteredOrSpace":"Değer Giriniz !!!","NonIntValue":"Geçerli Bir Sayı Giriniz !!!",
                          "ListEmpty":"Çalıştırmadan önce diziyi oluşturunuz !!!",
                          "SearchValueNotEntered":"Aranacak Değeri Giriniz !!!","ListItemNotSelected":"Listeden algoritmayı seçiniz !",
                          "SearchValueNotFound":"Aranılan Değer Listede Yok !",
                          "ArrayValueTooHigh":"Verilen dizi değeri maksimum değerden fazla !!!"
                          }
        self.resultDict = {"index": 0,"array":self.storedList}

    isFinishedSignal = pyqtSignal(object)

    def setUI(self):
        self.mainWindow = QWidget()
        self.numberBox =QLineEdit()
        self.numberBox.setPlaceholderText("Sayı giriniz :(max 100 000)")
        self.numberBox.setFixedWidth(150)
        self.randomButton =QPushButton("Rastgele Sayı Üret")
        self.randomButton.setEnabled(False)
        self.runButton = QPushButton("Çalıştır")
        self.runButton.setEnabled(False)
        self.listRadio = QRadioButton("Listeleme")
        self.searchRadio = QRadioButton("Arama")
        self.listList = QListWidget()
        self.searchlist = QListWidget()
        self.mainLayout = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.vbox1 = QVBoxLayout()



        self.mainWindow.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.hbox1)
        self.mainLayout.addLayout(self.hbox2)
        self.hbox1.addWidget(self.listRadio)
        self.hbox1.addWidget(self.searchRadio)
        self.hbox1.addWidget(self.numberBox)
        self.hbox2.addWidget(self.listList)
        self.hbox2.addWidget(self.searchlist)
        self.vbox1.addWidget(self.randomButton)
        self.vbox1.addWidget(self.runButton)
        self.hbox2.addLayout(self.vbox1)


        self.setLists()
        self.listRadio.toggle()
        self.listRadioToggled()
        self.listRadio.toggled.connect(lambda :self.listRadioToggled())
        self.searchRadio.toggled.connect(lambda :self.searchRadioToggled())
        self.numberBox.returnPressed.connect(lambda: self.generateRandNum())
        self.randomButton.clicked.connect(lambda: self.generateRandNum())
        self.runButton.clicked.connect(lambda: self.runIt())



        self.setWindowTitle("Algoritma Analizi Projesi")
        self.setFixedWidth(600)
        self.setFixedHeight(400)
        self.setCentralWidget(self.mainWindow)



    def setLists(self):

        self.listList.addItem("   __select an algorithm__")
        self.listList.addItem("Insertion Sort")
        self.listList.addItem("Merge Sort")
        self.listList.addItem("Heap Sort")
        self.listList.addItem("Quick Sort")
        self.listList.addItem("Counting Sort")
        self.listList.addItem("Bucket Sort")
        self.listList.addItem("Radix Sort")
        self.searchlist.addItem("   __select an algorithm__")
        self.searchlist.addItem("Linear Search")
        self.searchlist.addItem("Binary Search")
        self.currentItem = self.listList.item(0)
        self.listList.setCurrentItem(self.listList.item(0))
        self.searchlist.setCurrentItem(self.searchlist.item(0))
        self.searchlist.clicked.connect(lambda : self.searchlistItemClicked())
        self.listList.clicked.connect(lambda : self.listListItemClicked())
        return

    def searchlistItemClicked(self):
        self.currentItem= self.searchlist.currentItem().text()
        self.resultDict["currentAlgorithm"] = self.currentItem
        if self.currentItem == "   __select an algorithm__":
            self.randomButton.setEnabled(False)
        else :
            self.randomButton.setEnabled(True)
        return
    def listListItemClicked(self):
        self.currentItem= self.listList.currentItem().text()
        self.resultDict["currentAlgorithm"] = self.currentItem
        if self.currentItem == "   __select an algorithm__":
            self.randomButton.setEnabled(False)
        else :
            self.randomButton.setEnabled(True)
        return
    def listRadioToggled(self):
        self.listList.setEnabled(True)
        self.searchlist.setEnabled(False)
        self.isSearch = False
        self.resultDict["isSearch"] = self.isSearch
        return


    def searchRadioToggled(self):
        self.listList.setEnabled(False)
        self.searchlist.setEnabled(True)
        self.isSearch = True
        self.resultDict["isSearch"] = self.isSearch
        return


    def generateRandNum(self):
        import threading
        try:
            if int(self.numberBox.text().strip()) >100000:
                self._failed(self.errorDict["ArrayValueTooHigh"])
                self.numberBox.clear()
                return
        except Exception as e :
            errorMessage = self.errorDict["NonIntValue"]
            self._failed(errorMessage)
        else :
            self.mainWindow.setEnabled(False)
            self.t1 =threading.Thread(target=self._generate)
            self.t1.start()
            self.isFinishedSignal.connect(self.setActive)





    def setActive(self,val):

        if type(val) is str :
            self._failed(val)
        self.mainWindow.setEnabled(True)




    def _generate(self):
        import random

        self.storedList = []
        self.unsortedList = []
        if self.numberBox.text().strip() == "":
            errorMessage = self.errorDict["ValueNotEnteredOrSpace"]
            self.isFinishedSignal.emit(errorMessage)
            return


        try:
            arrayLength = int(self.numberBox.text().strip())
            for i in range(0, arrayLength + 1):
                if self.resultDict["currentAlgorithm"] == "Bucket Sort" :
                    randNum = round(random.random(),4)
                else :

                    randNum = random.randint(0,arrayLength +1)
                self.storedList.append(randNum)
                self.unsortedList.append(randNum)
        except:
            errorMessage = self.errorDict["NonIntValue"]
            self.isFinishedSignal.emit(errorMessage)

        else:
            self.runButton.setEnabled(1)
            self.isFinishedSignal.emit(100)


    def runIt(self):


        self.resultDict["dataset"] = self.unsortedList
        if self.isSearch :
            self.resultDict["searchValue"] = self._getsearchValue()
            if self.resultDict["searchValue"] == "":
                errorMessage = self.errorDict["ValueNotEnteredOrSpace"]
                self._failed(errorMessage)
                return
            algorithm = LSAlgorithms()
            if self.currentItem == "Linear Search":
                tstart = time.time()
                time.sleep(0.1)
                self.resultDict["index"] = algorithm._linearSearch(self.storedList,self.resultDict["searchValue"])
                tstop  = time.time()

            elif self.currentItem == "Binary Search":
                self.storedList = algorithm.insertionSort(self.storedList)
                tstart = time.time()
                time.sleep(0.1)
                self.resultDict["index"] = algorithm._binarySearch(self.storedList,self.resultDict["searchValue"])
                tstop  = time.time()

            else :
                self._failed(self.errorDict["ListItemNotSelected"])
                return
            self.resultDict["time"] = round((tstop-tstart-0.1),6)
            self.resultDict["array"] = self.storedList
            self._searchWindow()

        else :
            algorithm = LSAlgorithms()
            if self.currentItem == "Insertion Sort":
                tstart = time.time()
                time.sleep(0.1)
                self.storedList= algorithm.insertionSort(self.storedList)
                tstop = time.time()

            elif self.currentItem == "Merge Sort":
                tstart = time.time()
                time.sleep(0.1)
                self.storedList =algorithm.mergeSort(self.storedList)
                tstop = time.time()
            elif self.currentItem == "Heap Sort":
                tstart = time.time()
                time.sleep(0.1)
                algorithm.heapSort()
                tstop = time.time
            elif self.currentItem  == "Quick Sort":
                tstart = time.time()
                time.sleep(0.1)
                algorithm.quickSort()
                tstop = time.time
            elif self.currentItem == "Counting Sort":
                tstart = time.time()
                time.sleep(0.1)
                algorithm.countingSort()
                tstop = time.time()
            elif self.currentItem == "Bucket Sort":
                tstart = time.time()
                time.sleep(0.1)
                self.storedList = algorithm.bucketSort(self.storedList)
                tstop = time.time()
            elif self.currentItem == "Radix Sort":
                tstart = time.time()
                time.sleep(0.1)
                algorithm.radixSort()
                tstop = time.time()

            else:
                self._failed(self.errorDict["ListItemNotSelected"])
                return
            self.resultDict["time"] = round((tstop-tstart-0.1), 6)
            self.resultDict["array"] = self.storedList
            self._searchWindow()

            return



    def _failed(self,message):
        self.errorMessage = QErrorMessage()
        self.errorMessage.showMessage(message)
        self.errorMessage.setWindowTitle("Hata")
        self.errorMessage.exec()

    def _getsearchValue(self):

        sValue , isok = QInputDialog.getText(self,'Değer Gir','Aranacak Değeri Gir :')
        if isok:

            try:

                sValue = int(sValue)

            except:

                self._failed(self.errorDict["NonIntValue"])
                return
            else:
                return sValue

    def _searchWindow(self):
        if(self.resultDict["index"] == -1) :
            self._failed(self.errorDict["SearchValueNotFound"])
        else:

            resWindow = resultWindow(self.resultDict)
            resWindow.exec()
            if  not self.isSearch or self.resultDict["currentAlgorithm"] == "Binary Search" :
                self.runButton.setEnabled(False)
                self.storedList = []




class LSAlgorithms():
    def __init__(self):
        return



    def _binarySearch(self,arr,val): #working
        first = 0
        last = len(arr) - 1

        while (first <= last) :
            mid = (first + last) // 2
            if arr[mid] == val:
                return mid
            elif int(val) < arr[mid]:
                    last = mid - 1
            else:
                    first = mid + 1
        return -1



    def _linearSearch(self,arr,val): #working
        for i in range(len(arr)):
            if arr[i] == val :
                return i
        return -1



    def insertionSort(self,arr): #working
        for i in range(1, len(arr)):
            j = i - 1
            next_item = arr[i]
            while arr[j] > next_item and j >= 0:
                arr[j + 1] = arr[j]
                j = j - 1
                arr[j + 1] = next_item

        return arr



    def bucketSort(self,x): #working
        arr = []
        slot_num = 10  # 10 means 10 slots, each
        # slot's size is 0.1
        for i in range(slot_num):
            arr.append([])

            # Put array elements in different buckets
        for j in x:
            index_b = int(slot_num * j)
            arr[index_b].append(j)

            # Sort individual buckets
        for i in range(slot_num):
            arr[i] = self.insertionSort(arr[i])

            # concatenate the result
        k = 0
        for i in range(slot_num):
            for j in range(len(arr[i])):
                x[k] = arr[i][j]
                k += 1
        return x




    def countingSort(self,array, place): #not working
        size = len(array)
        output = [0] * size
        count = [0] * 10

        # Calculate count of elements
        for i in range(0, size):
            index = array[i] // place
            count[index % 10] += 1

        # Calculate cummulative count
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Place the elements in sorted order
        i = size - 1
        while i >= 0:
            index = array[i] // place
            output[count[index % 10] - 1] = array[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(0, size):
            array[i] = output[i]




    def mergeSort(self,arr): #working
        if len(arr)== 1 :
            return arr

        middle = len(arr)//2
        left_arr = arr[:middle]
        right_arr = arr[middle:]

        left_arr = self.mergeSort(left_arr)
        right_arr = self.mergeSort(right_arr)
        return list(self.merge(left_arr,right_arr))

    def merge(self,l,r):
        arr = []
        while len(l)!=0 and len(r)!=0:
            if l[0]<r[0]:
                arr.append(l[0])
                l.remove(l[0])
            else :
                arr.append(r[0])
                r.remove(r[0])
        if len(l) == 0 :
            arr += r

        else :
            arr += l

        return arr




    def radixSort(self,array): #not working
        # Get maximum element
        max_element = max(array)

        # Apply counting sort to sort elements based on place value.
        place = 1
        while max_element // place > 0:
            self.countingSort(array, place)
            place *= 10

class resultWindow(QDialog):
    def __init__(self,dict):
        super().__init__()
        self.dict =dict
        self.setUI()

    def setUI(self):
        self.setWindowTitle("Arama Sonuçları")
        isTrue = self.dict["isSearch"]
        if isTrue :
            dBoxFormLayout = QFormLayout()



            indexLine = QLineEdit()
            indexLine.setReadOnly(True)

            sValueLine = QLineEdit()
            sValueLine.setReadOnly(True)

            timeValueLine =QLineEdit()
            timeValueLine.setReadOnly(True)

            algovalueLine =QLineEdit()
            algovalueLine.setReadOnly(True)

            datasetValueLine = QTextEdit()
            datasetValueLine.setReadOnly(True)

            #arrayValueText= QTextEdit()
            #arrayValueText.setReadOnly(True)


            dBoxFormLayout.addRow(QLabel("Current Algorithm : "),algovalueLine)

            dBoxFormLayout.addRow(QLabel("Current Dataset :"), datasetValueLine)

            dBoxFormLayout.addRow(QLabel("Searched Value: "),sValueLine)

            dBoxFormLayout.addRow(QLabel("Index Value :"), indexLine)

            dBoxFormLayout.addRow(QLabel("Algorithm Time : "),timeValueLine)




            #dBoxFormLayout.addRow(QLabel("Array :"))

            algovalueLine.setText(str(self.dict["currentAlgorithm"]))

            datasetValueLine.setText(str(self.dict["dataset"]))

            sValueLine.setText(str(self.dict["searchValue"]))

            indexLine.setText(str(self.dict["index"]))

            if str(self.dict["currentAlgorithm"]) == "Binary Search":
                arrayValueText = QTextEdit()
                arrayValueText.setReadOnly(True)
                dBoxFormLayout.addRow(QLabel("Array :"), arrayValueText)
                arrayValueText.setText(str(self.dict["array"]))

            timeValueLine.setText(str(self.dict["time"])+" second(s)")






            self.setLayout(dBoxFormLayout)
        else :
            dBoxFormLayout = QFormLayout()


            timeValueLine = QLineEdit()
            timeValueLine.setReadOnly(True)

            algovalueLine = QLineEdit()
            algovalueLine.setReadOnly(True)

            datasetvalueLine = QTextEdit()
            datasetvalueLine.setReadOnly(True)

            arrayValueText= QTextEdit()
            arrayValueText.setReadOnly(True)

            dBoxFormLayout.addRow(QLabel("Current Algorithm : "), algovalueLine)

            dBoxFormLayout.addRow(QLabel("Algorithm Time : "), timeValueLine)

            dBoxFormLayout.addRow(QLabel("Current Dataset: "),datasetvalueLine)

            dBoxFormLayout.addRow(QLabel("Array :"),arrayValueText)

            algovalueLine.setText(str(self.dict["currentAlgorithm"]))

            timeValueLine.setText(str(self.dict["time"]) + " second(s)")

            datasetvalueLine.setText(str(self.dict["dataset"]))

            arrayValueText.setText(str(self.dict["array"]))

            self.setLayout(dBoxFormLayout)








if __name__ == "__main__" :
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setUI()
    window.show()
    sys.exit(app.exec())