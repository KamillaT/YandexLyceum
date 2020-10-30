import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem, QMessageBox
from ui_4 import Ui_Form
import sqlite3

class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films.db")
        self.pushButton.clicked.connect(self.update_result)
        self.deleteButton.clicked.connect(self.update_elems)
    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        que = "SELECT * FROM Films WHERE " + self.textEdit.toPlainText()
        result = cur.execute(que).fetchall()

        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))

        # Заполнили таблицу полученными элементами
        for i,elem in enumerate(result):
            for j,val in enumerate(elem):
                self.tableWidget.setItem(i,j,QTableWidgetItem(str(val)))

    def generate_new_elems(self,ids):
        cur = self.con.cursor()
        for i in ids:
            data = cur.execute("SELECT * from films where id = {}".format(i)).fetchone()
            new_data = (data[0], data[1][::-1],data[2]+1000,data[3],data[4]*2)
            cur.execute("DELETE FROM films where id = {}".format(data[0]))
            cur.execute("INSERT INTO films VALUES (?,?,?,?,?)",new_data)
        self.con.commit()
            
            
    def update_elems(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i,0).text() for i in rows]
        valid = QMessageBox.question(self,'',"Действительно заменить элементы с id "+",".join(ids),QMessageBox.Yes,QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.generate_new_elems(ids)

    

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
