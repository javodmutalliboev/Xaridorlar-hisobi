import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)

import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="javod", password="hHh(26Y2%C~w", database="online_magazin"
)

cursor = conn.cursor()


class XaridorlarHisobiWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Xaridorlar hisobi")

        v_layout = QVBoxLayout()

        self.table = QTableWidget()

        h_layout = QHBoxLayout()

        distinct_button = QPushButton("DISTINCT")
        distinct_button.clicked.connect(self.distinct)
        h_layout.addWidget(distinct_button)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.yuklash)
        h_layout.addWidget(reset_button)

        h_layout2 = QHBoxLayout()
        count_button = QPushButton("COUNT xaridlar soni")
        count_button.clicked.connect(self.count)
        h_layout2.addWidget(count_button)

        left_join_button = QPushButton("LEFT JOIN xaridlar")
        left_join_button.clicked.connect(self.left_join_xaridlar)
        h_layout2.addWidget(left_join_button)

        h_layout3 = QHBoxLayout()
        sum_button = QPushButton("Umumiy xaridlar summasi")
        sum_button.clicked.connect(self.sum)
        h_layout3.addWidget(sum_button)

        min_button = QPushButton("Minimum xarid summasi")
        min_button.clicked.connect(self.min)
        h_layout3.addWidget(min_button)

        max_button = QPushButton("Maximum xarid summasi")
        max_button.clicked.connect(self.max)
        h_layout3.addWidget(max_button)

        # left_join_button = QPushButton("LEFT JOIN xaridlar")
        # left_join_button.clicked.connect(self.left_join_xaridlar)
        # h_layout2.addWidget(left_join_button)

        v_layout.addWidget(self.table)
        v_layout.addLayout(h_layout)
        v_layout.addLayout(h_layout2)
        v_layout.addLayout(h_layout3)
        self.setLayout(v_layout)

        self.setStyleSheet(
            """
                QWidget {
                    font-size: 22px;
                }
            """
        )

        self.yuklash()

    def min(self):
        try:
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(
                ["Xaridor ismi", "Minimum xarid summasi"]
            )
            cursor.execute(
                "SELECT xdor.xaridor_ismi, \
                      MIN(x.xarid_narxi) FROM \
                          xaridorlar AS xdor LEFT \
                              JOIN xaridlar AS x ON \
                                  xdor.id = x.xaridor_id \
                                      GROUP BY xdor.xaridor_ismi;"
            )
            self.table.setRowCount(0)
            for row_idx, (xaridor_ismi, min_xarid) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(xaridor_ismi))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(min_xarid)))

        except Exception as exp:
            print(exp)

    def max(self):
        try:
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(
                ["Xaridor ismi", "Maximum xarid summasi"]
            )
            cursor.execute(
                "SELECT xdor.xaridor_ismi, \
                      MAX(x.xarid_narxi) FROM \
                          xaridorlar AS xdor LEFT \
                              JOIN xaridlar AS x ON \
                                  xdor.id = x.xaridor_id \
                                      GROUP BY xdor.xaridor_ismi;"
            )
            self.table.setRowCount(0)
            for row_idx, (xaridor_ismi, max_xarid) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(xaridor_ismi))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(max_xarid)))

        except Exception as exp:
            print(exp)

    def sum(self):
        try:
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(
                ["Xaridor ismi", "Umumiy xaridlari summasi"]
            )
            cursor.execute(
                "SELECT xdor.xaridor_ismi, \
                      SUM(x.xarid_narxi) FROM \
                          xaridorlar AS xdor LEFT \
                              JOIN xaridlar AS x ON \
                                  xdor.id = x.xaridor_id \
                                      GROUP BY xdor.xaridor_ismi;"
            )
            self.table.setRowCount(0)
            for row_idx, (xaridor_ismi, xaridlari_sum) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(xaridor_ismi))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(xaridlari_sum)))

        except Exception as exp:
            print(exp)

    def left_join_xaridlar(self):
        try:
            self.reset_table_structure()
            cursor.execute(
                "SELECT x.id AS 'xarid id', xdor.xaridor_ismi \
                      FROM xaridorlar as xdor LEFT JOIN \
                          xaridlar as x ON xdor.id = x.xaridor_id;"
            )
            self.table.setRowCount(0)
            for row_idx, (xarid_id, xaridor_ismi) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(xarid_id)))
                self.table.setItem(row_idx, 1, QTableWidgetItem(xaridor_ismi))

        except Exception as exp:
            print(exp)

    def count(self):
        try:
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Xaridor ismi", "Xaridlari soni"])
            cursor.execute(
                "SELECT xdor.xaridor_ismi, COUNT(x.xaridor_id) \
                      AS xaridlari_soni FROM xaridorlar AS \
                          xdor LEFT JOIN xaridlar AS x ON \
                              xdor.id = x.xaridor_id GROUP BY xdor.xaridor_ismi;"
            )
            self.table.setRowCount(0)
            for row_idx, (xaridor_ismi, xaridlari_soni) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(xaridor_ismi))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(xaridlari_soni)))

        except Exception as exp:
            print(exp)

    def distinct(self):
        try:
            self.reset_table_structure()
            cursor.execute(
                "SELECT DISTINCT xdor.xaridor_ismi FROM \
                      xaridorlar AS xdor LEFT JOIN xaridlar \
                          AS x ON xdor.id = x.xaridor_id;"
            )
            self.table.setRowCount(0)
            for row_idx, (xaridor_ismi,) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 1, QTableWidgetItem(xaridor_ismi))

        except Exception as exp:
            print(exp)

    def reset_table_structure(self):
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Xarid IDsi", "Xaridor ismi"])

    def yuklash(self):
        try:
            self.reset_table_structure()
            cursor.execute(
                "SELECT x.id, xdor.xaridor_ismi FROM xaridorlar \
                      AS xdor LEFT JOIN xaridlar AS x ON xdor.id = x.xaridor_id;"
            )
            self.table.setRowCount(0)
            for row_idx, (xarid_id, xaridor_ismi) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(xarid_id)))
                self.table.setItem(row_idx, 1, QTableWidgetItem(xaridor_ismi))

        except Exception as exp:
            print(exp)


def main():
    app = QApplication(sys.argv)
    window = XaridorlarHisobiWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
