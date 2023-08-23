import os
import sys
import uic
from os import system
#######################

#############################
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QHeaderView, QDialog, QStackedWidget

from Ui_AISS import *

# IMPORT Custom widgets
from Custom_Widgets.Widgets import *
import sqlite3

###################################

from qt_material import apply_stylesheet

############################SHADOW ELEMENTS##############################################
shadow_elements = {
    "tool_container",
    "tool_page_car",
    "tool_page_sale"
}
flag = 0


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        
        

        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        loadJsonStyle(self, self.ui)
        ######################### SLICE ########################
        self.ui.clientsBtn.clicked.connect(lambda: self.ui.moveContainer.expandMenu())
        self.ui.saleBtn.clicked.connect(lambda: self.ui.moveContainer.expandMenu())
        self.ui.carBtn.clicked.connect(lambda: self.ui.moveContainer.expandMenu())
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.moveContainer.expandMenu())
        self.ui.clientsBtn.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.saleBtn.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.carBtn.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.searchBtn_2.clicked.connect(lambda: self.ui.searchWidget.expandMenu())
        self.ui.searchBtn_3.clicked.connect(lambda: self.ui.searchWidget.expandMenu())
        self.ui.saveBtn.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.saveBtn_2.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.saveBtn_3.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.deleteBtn.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.deleteRowBtn_2.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.deleteRowBtn_3.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.addRowBtn.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.addRowBtn_2.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.addRowBtn_3.clicked.connect(lambda: self.ui.searchWidget.collapseMenu())
        self.ui.searchBtn.clicked.connect(self.loaddata)
        
        
        
        ######################### NAVIGATION ############################################
        self.ui.clientsBtn.clicked.connect(
            lambda: self.ui.menuStackedWidget.setCurrentWidget(self.ui.tool_page_clients))
        self.ui.clientsBtn.clicked.connect(lambda: self.ui.tablesStackedWidget.setCurrentWidget(self.ui.clients_page))
        self.ui.carBtn.clicked.connect(lambda: self.ui.menuStackedWidget.setCurrentWidget(self.ui.tool_page_car))
        self.ui.carBtn.clicked.connect(lambda: self.ui.tablesStackedWidget.setCurrentWidget(self.ui.car_page))
        self.ui.searchBtnTool.clicked.connect(
            lambda: self.ui.tablesStackedWidget.setCurrentWidget(self.ui.search_page_clients))
        self.ui.searchBtn_2.clicked.connect(
            lambda: self.ui.tablesStackedWidget.setCurrentWidget(self.ui.search_page_car))
        self.ui.saleBtn.clicked.connect(lambda: self.ui.tablesStackedWidget.setCurrentWidget(self.ui.sale_page))
        self.ui.saleBtn.clicked.connect(
            lambda: self.ui.menuStackedWidget.setCurrentWidget(self.ui.tool_page_sale))
        self.ui.searchBtn_3.clicked.connect(
            lambda: self.ui.tablesStackedWidget.setCurrentWidget(self.ui.search_page_sale))
        self.ui.settingsBtn.clicked.connect(
            lambda: self.ui.menuStackedWidget.setCurrentWidget(self.ui.settings_page))
        self.ui.autorBtn.clicked.connect(
            lambda: self.ui.tablesStackedWidget.setCurrentWidget(self.ui.dark_page))

        ######################## SAVE IN DATA  #####################################
        self.ui.saveBtn.clicked.connect(self.deleteDATA)
        self.ui.saveBtn.clicked.connect(self.readtableData)
        self.ui.saveBtn_2.clicked.connect(self.deleteDATA_2)
        self.ui.saveBtn_2.clicked.connect(self.readtableData_2)
        self.ui.saveBtn_3.clicked.connect(self.deleteDATA_3)
        self.ui.saveBtn_3.clicked.connect(self.readtableData_3)
        self.ui.updateBtn.clicked.connect(self.loaddata)
        self.shadow()
        ######################## ENABLE SORTING ######################################
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget_2.setSortingEnabled(True)
        self.ui.tableWidget_5.setSortingEnabled(True)
        ################################ ADD ROW ####################################################
        self.ui.addRowBtn.clicked.connect(lambda: self.ui.tableWidget.insertRow(self.ui.tableWidget.currentRow()))
        self.ui.addRowBtn_2.clicked.connect(lambda: self.ui.tableWidget_2.insertRow(self.ui.tableWidget_2.currentRow()))
        self.ui.addRowBtn_3.clicked.connect(lambda: self.ui.tableWidget_5.insertRow(self.ui.tableWidget_5.currentRow()))
        ################################ DELETE ROW ##################################################
        self.ui.deleteBtn.clicked.connect(lambda: self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow()))
        self.ui.deleteRowBtn_2.clicked.connect(
            lambda: self.ui.tableWidget_2.removeRow(self.ui.tableWidget_2.currentRow()))
        self.ui.deleteRowBtn_3.clicked.connect(
            lambda: self.ui.tableWidget_5.removeRow(self.ui.tableWidget_5.currentRow()))
        # LOAD DATA
        self.loaddata()

    def loaddata(self):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget_2.setRowCount(0)
        self.ui.tableWidget_3.setRowCount(0)
        self.ui.tableWidget_4.setRowCount(0)
        self.ui.tableWidget_5.setRowCount(0)
        self.ui.tableWidget_6.setRowCount(0)
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        ################ Вывод информации на таблицу и поиск по клиентам ########################################
        self.ui.tableWidget.setRowCount(25)
        self.ui.tableWidget_2.setRowCount(25)
        self.ui.tableWidget_3.setRowCount(25)
        self.ui.tableWidget_4.setRowCount(25)
        self.ui.tableWidget_5.setRowCount(25)
        self.ui.tableWidget_6.setRowCount(25)
        tablerow_clients = 0
        tablerow_car = 0
        tablerow_sale = 0
        query_clients = '''SELECT * FROM Клиенты'''
        for row in cur.execute(query_clients):
            self.ui.tableWidget.setItem(tablerow_clients, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tableWidget.setItem(tablerow_clients, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tableWidget.setItem(tablerow_clients, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tableWidget.setItem(tablerow_clients, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tableWidget.setItem(tablerow_clients, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.tableWidget.setItem(tablerow_clients, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            tablerow_clients += 1
        search_row = 0
        rowcount = self.ui.tableWidget.rowCount()
        columnCount = self.ui.tableWidget.columnCount()
        for row in range(rowcount):
            rowData = []
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget.item(row, column)
                if (widgetItem and widgetItem.text()):
                    rowData.append(widgetItem.text())
                else:
                    rowData.append('')
            if self.ui.lineEdit.text() in rowData:
                self.ui.tableWidget_3.setItem(search_row, 0, QtWidgets.QTableWidgetItem(rowData[0]))
                self.ui.tableWidget_3.setItem(search_row, 1, QtWidgets.QTableWidgetItem(rowData[1]))
                self.ui.tableWidget_3.setItem(search_row, 2, QtWidgets.QTableWidgetItem(rowData[2]))
                self.ui.tableWidget_3.setItem(search_row, 3, QtWidgets.QTableWidgetItem(rowData[3]))
                self.ui.tableWidget_3.setItem(search_row, 4, QtWidgets.QTableWidgetItem(rowData[4]))
                self.ui.tableWidget_3.setItem(search_row, 5, QtWidgets.QTableWidgetItem(rowData[5]))
                search_row += 1
        self.ui.tableWidget_3.setRowCount(search_row)
        ################ Вывод информации на таблицу и поиск по авто ########################################
        query_car = '''SELECT * FROM Автомобили'''
        for row_2 in cur.execute(query_car):
            self.ui.tableWidget_2.setItem(tablerow_car, 0, QtWidgets.QTableWidgetItem(str(row_2[0])))
            self.ui.tableWidget_2.setItem(tablerow_car, 1, QtWidgets.QTableWidgetItem(str(row_2[1])))
            self.ui.tableWidget_2.setItem(tablerow_car, 2, QtWidgets.QTableWidgetItem(str(row_2[2])))
            self.ui.tableWidget_2.setItem(tablerow_car, 3, QtWidgets.QTableWidgetItem(str(row_2[3])))
            self.ui.tableWidget_2.setItem(tablerow_car, 4, QtWidgets.QTableWidgetItem(str(row_2[4])))
            self.ui.tableWidget_2.setItem(tablerow_car, 5, QtWidgets.QTableWidgetItem(str(row_2[5])))
            tablerow_car += 1
        search_row_car = 0
        rowcount_car = self.ui.tableWidget_2.rowCount()
        columnCount_car = self.ui.tableWidget_2.columnCount()
        for row in range(rowcount_car):
            rowData_car = []
            for column in range(columnCount_car):
                widgetItem = self.ui.tableWidget_2.item(row, column)
                if (widgetItem and widgetItem.text()):
                    rowData_car.append(widgetItem.text())
                else:
                    rowData_car.append('')
            if self.ui.lineEdit.text() in rowData_car:
                self.ui.tableWidget_4.setItem(search_row_car, 0, QtWidgets.QTableWidgetItem(rowData_car[0]))
                self.ui.tableWidget_4.setItem(search_row_car, 1, QtWidgets.QTableWidgetItem(rowData_car[1]))
                self.ui.tableWidget_4.setItem(search_row_car, 2, QtWidgets.QTableWidgetItem(rowData_car[2]))
                self.ui.tableWidget_4.setItem(search_row_car, 3, QtWidgets.QTableWidgetItem(rowData_car[3]))
                self.ui.tableWidget_4.setItem(search_row_car, 4, QtWidgets.QTableWidgetItem(rowData_car[4]))
                self.ui.tableWidget_4.setItem(search_row_car, 5, QtWidgets.QTableWidgetItem(rowData_car[5]))
                search_row_car += 1
        self.ui.tableWidget_4.setRowCount(search_row_car)
        ########################### Вывод информации на таблицу и поиск по продажам #####################################
        query_sale = '''SELECT * FROM Продажи'''
        for row_3 in cur.execute(query_sale):
            self.ui.tableWidget_5.setItem(tablerow_sale, 0, QtWidgets.QTableWidgetItem(str(row_3[0])))
            self.ui.tableWidget_5.setItem(tablerow_sale, 1, QtWidgets.QTableWidgetItem(str(row_3[1])))
            self.ui.tableWidget_5.setItem(tablerow_sale, 2, QtWidgets.QTableWidgetItem(str(row_3[2])))
            self.ui.tableWidget_5.setItem(tablerow_sale, 3, QtWidgets.QTableWidgetItem(str(row_3[3])))
            self.ui.tableWidget_5.setItem(tablerow_sale, 4, QtWidgets.QTableWidgetItem(str(row_3[4])))
            tablerow_sale += 1
        search_row_sale = 0
        rowcount_sale = self.ui.tableWidget_5.rowCount()
        columnCount_sale = self.ui.tableWidget_5.columnCount()
        for row in range(rowcount_sale):
            rowData_sale = []
            for column in range(columnCount_sale):
                widgetItem = self.ui.tableWidget_5.item(row, column)
                if (widgetItem and widgetItem.text()):
                    rowData_sale.append(widgetItem.text())
                else:
                    rowData_sale.append('')
            if self.ui.lineEdit.text() in rowData_sale:
                self.ui.tableWidget_6.setItem(search_row_sale, 0, QtWidgets.QTableWidgetItem(rowData_sale[0]))
                self.ui.tableWidget_6.setItem(search_row_sale, 1, QtWidgets.QTableWidgetItem(rowData_sale[1]))
                self.ui.tableWidget_6.setItem(search_row_sale, 2, QtWidgets.QTableWidgetItem(rowData_sale[2]))
                self.ui.tableWidget_6.setItem(search_row_sale, 3, QtWidgets.QTableWidgetItem(rowData_sale[3]))
                self.ui.tableWidget_6.setItem(search_row_sale, 4, QtWidgets.QTableWidgetItem(rowData_sale[4]))
                search_row_sale += 1
        self.ui.tableWidget_6.setRowCount(search_row_sale)
        connection.close()

    ###############SAVE IN DATA FOR CLIENTS######################
    def deleteDATA(self):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        queryDelete = '''delete FROM Клиенты;
        delete FROM sqlite_sequence WHERE name= 'Клиенты' '''
        connection.executescript(queryDelete)
        connection.commit()
        connection.close()

    def readtableData(self):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        rowcount = self.ui.tableWidget.rowCount()
        columnCount = self.ui.tableWidget.columnCount()
        for row in range(rowcount):
            rowData = []
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget.item(row, column)
                if (widgetItem and widgetItem.text()):
                    rowData.append(widgetItem.text())
                else:
                    rowData.append('')
            rowData = rowData[1:]
            self.insertRowInDB(rowData)
        connection.close()

    def insertRowInDB(self, rowData):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        queryStr = """INSERT INTO Клиенты ("surname", "name", "lastname", "address", "phone") VALUES(?,?,?,?,?)"""
        if "" not in rowData:
            cur.execute(queryStr, rowData)
            connection.commit()
        connection.close()

    ############### SAVE IN DATA FOR CARS ######################
    def deleteDATA_2(self):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        queryDelete_2 = '''delete FROM Автомобили;
        delete FROM sqlite_sequence WHERE name = 'Автомобили' '''
        connection.executescript(queryDelete_2)
        connection.commit()
        connection.close()

    def readtableData_2(self):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        rowcount_2 = self.ui.tableWidget_2.rowCount()
        columnCount_2 = self.ui.tableWidget_2.columnCount()
        for row in range(rowcount_2):
            rowData_2 = []
            for column in range(columnCount_2):
                widgetItem_2 = self.ui.tableWidget_2.item(row, column)
                if (widgetItem_2 and widgetItem_2.text()):
                    rowData_2.append(widgetItem_2.text())
                else:
                    rowData_2.append('')
            rowData_2 = rowData_2[1:]
            self.insertRowInDB_2(rowData_2)
        connection.close()

    def insertRowInDB_2(self, rowData_2):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        queryStr_2 = """INSERT INTO Автомобили ("make", "model", "color", "probeg", "year") VALUES (?,?,?,?,?)"""
        if "" not in rowData_2:
            cur.execute(queryStr_2, rowData_2)
            connection.commit()
        connection.close()
        ############### SAVE IN DATA FOR SALES ######################

    def deleteDATA_3(self):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        queryDelete_3 = '''delete FROM Продажи; 
        delete FROM sqlite_sequence WHERE name = 'Продажи' '''
        connection.executescript(queryDelete_3)
        connection.commit()
        connection.close()

    def readtableData_3(self):
        rowDateGlobal = []
        rowPriceGlobal = []
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        rowcount_3 = self.ui.tableWidget_5.rowCount()
        columnCount_3 = self.ui.tableWidget_5.columnCount()
        for row in range(rowcount_3):
            rowDate = []
            rowPrice = []
            rowData_3 = []
            for column in range(columnCount_3):
                widgetItem_3 = self.ui.tableWidget_5.item(row, column)
                if (widgetItem_3 and widgetItem_3.text()):
                    rowData_3.append(widgetItem_3.text())
                    rowDate.append(widgetItem_3.text())
                    rowPrice.append(widgetItem_3.text())
                else:
                    rowData_3.append('')
                    rowDate.append('')
                    rowPrice.append('')

            rowData_3 = rowData_3[1:]
            rowDate = rowDate[3:4]
            rowPrice = rowPrice[4:]
            if '' not in rowDate:
                rowDateGlobal.append(rowDate)
            if '' not in rowPrice:
                rowPriceGlobal.append(rowPrice)
            self.insertRowInDB_3(rowData_3)
        print(rowDateGlobal)
        print(rowPriceGlobal)
        connection.close()

    def insertRowInDB_3(self, rowData_3):
        connection = sqlite3.connect('carsale.sqlite')
        cur = connection.cursor()
        queryStr_3 = """INSERT INTO Продажи ("id_car", "id_client", "date_sale", "price") 
        VALUES (?,?,?,?)"""
        if "" not in rowData_3:
            cur.execute(queryStr_3, rowData_3)
            connection.commit()
        connection.close()

    ####################### SHADOW EFFECTS ########################################
    def shadow(self):
        for x in shadow_elements:
            effect = QtWidgets.QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(120)
            effect.setXOffset(0)
            effect.setYOffset(0)
            effect.setColor(QColor(0, 0, 0, 255))
            getattr(self.ui, x).setGraphicsEffect(effect)
        
        self.show()
        self.ui.lineEdit.echoMode()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
