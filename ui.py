from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QMessageBox,
    QSpinBox, QDoubleSpinBox, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from database import Database
from calculator import PortfolioCalculator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle('Stock Portfolio Manager')
        self.setGeometry(100, 100, 1200, 700)
        
        self.init_ui()
    
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        title = QLabel('Stock Portfolio Manager')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        capital_layout = QHBoxLayout()
        capital_label = QLabel('رأس المال (Capital):')
        capital_label.setMinimumWidth(150)
        self.capital_input = QDoubleSpinBox()
        self.capital_input.setMaximum(1000000000)
        self.capital_input.setMinimumWidth(200)
        self.add_capital_btn = QPushButton('إضافة رأس المال')
        self.add_capital_btn.clicked.connect(self.add_capital)
        capital_layout.addWidget(capital_label)
        capital_layout.addWidget(self.capital_input)
        capital_layout.addWidget(self.add_capital_btn)
        capital_layout.addStretch()
        layout.addLayout(capital_layout)
        
        transaction_layout = QHBoxLayout()
        
        stock_label = QLabel('اسم السهم:')
        stock_label.setMinimumWidth(100)
        self.stock_name_input = QLineEdit()
        self.stock_name_input.setPlaceholderText('مثال: AAPL')
        self.stock_name_input.setMinimumWidth(150)
        
        quantity_label = QLabel('الكمية:')
        quantity_label.setMinimumWidth(100)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(1000000)
        self.quantity_input.setMinimumWidth(150)
        
        buy_price_label = QLabel('سعر الشراء:')
        buy_price_label.setMinimumWidth(100)
        self.buy_price_input = QDoubleSpinBox()
        self.buy_price_input.setMaximum(1000000)
        self.buy_price_input.setMinimumWidth(150)
        
        self.add_transaction_btn = QPushButton('إضافة معاملة')
        self.add_transaction_btn.clicked.connect(self.add_transaction)
        
        transaction_layout.addWidget(stock_label)
        transaction_layout.addWidget(self.stock_name_input)
        transaction_layout.addWidget(quantity_label)
        transaction_layout.addWidget(self.quantity_input)
        transaction_layout.addWidget(buy_price_label)
        transaction_layout.addWidget(self.buy_price_input)
        transaction_layout.addWidget(self.add_transaction_btn)
        transaction_layout.addStretch()
        layout.addLayout(transaction_layout)
        
        stats_layout = QHBoxLayout()
        
        self.total_invested_label = QLabel('إجمالي المستثمر: 0')
        self.total_invested_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        
        self.current_value_label = QLabel('القيمة الحالية: 0')
        self.current_value_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        
        self.profit_loss_label = QLabel('الربح/الخسارة: 0')
        self.profit_loss_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        
        self.profit_loss_percent_label = QLabel('النسبة: 0%')
        self.profit_loss_percent_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        
        stats_layout.addWidget(self.total_invested_label)
        stats_layout.addWidget(self.current_value_label)
        stats_layout.addWidget(self.profit_loss_label)
        stats_layout.addWidget(self.profit_loss_percent_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            'ID', 'اسم السهم', 'الكمية', 'سعر الشراء', 'سعر البيع',
            'الحالة', 'الربح/الخسارة', 'النسبة %', 'إجراء'
        ])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 150)
        self.table.setColumnWidth(7, 100)
        self.table.setColumnWidth(8, 100)
        layout.addWidget(self.table)
        
        main_widget.setLayout(layout)
        self.load_transactions()
    
    def add_capital(self):
        amount = self.capital_input.value()
        if amount <= 0:
            QMessageBox.warning(self, 'تحذير', 'أدخل مبلغاً صحيحاً')
            return
        
        self.db.add_capital(amount)
        self.capital_input.setValue(0)
        QMessageBox.information(self, 'نجاح', f'تم إضافة {amount} رأس المال')
    
    def add_transaction(self):
        stock_name = self.stock_name_input.text().strip()
        quantity = self.quantity_input.value()
        buy_price = self.buy_price_input.value()
        
        if not stock_name or quantity <= 0 or buy_price <= 0:
            QMessageBox.warning(self, 'تحذير', 'أدخل بيانات صحيحة')
            return
        
        self.db.add_transaction(stock_name, quantity, buy_price)
        self.stock_name_input.clear()
        self.quantity_input.setValue(0)
        self.buy_price_input.setValue(0)
        
        self.load_transactions()
        QMessageBox.information(self, 'نجاح', 'تم إضافة المعاملة')
    
    def load_transactions(self):
        transactions = self.db.get_all_transactions()
        self.table.setRowCount(0)
        
        for transaction in transactions:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            transaction_id, stock_name, quantity, buy_price, sell_price, status, date_added, date_sold = transaction
            
            self.table.setItem(row, 0, QTableWidgetItem(str(transaction_id)))
            self.table.setItem(row, 1, QTableWidgetItem(stock_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(quantity)))
            self.table.setItem(row, 3, QTableWidgetItem(f'{buy_price:.2f}'))
            self.table.setItem(row, 4, QTableWidgetItem(f'{sell_price if sell_price else "-":.2f}' if sell_price else '-'))
            self.table.setItem(row, 5, QTableWidgetItem(status))
            
            calculator = PortfolioCalculator([transaction])
            profit_loss = calculator.calculate_profit_loss(transaction)
            profit_loss_percentage = calculator.calculate_profit_loss_percentage(transaction)
            
            if profit_loss is not None:
                self.table.setItem(row, 6, QTableWidgetItem(f'{profit_loss:.2f}'))
                self.table.setItem(row, 7, QTableWidgetItem(f'{profit_loss_percentage:.2f}%'))
            else:
                self.table.setItem(row, 6, QTableWidgetItem('-'))
                self.table.setItem(row, 7, QTableWidgetItem('-'))
            
            sell_btn = QPushButton('بيع')
            sell_btn.clicked.connect(lambda checked, tid=transaction_id: self.sell_dialog(tid))
            self.table.setCellWidget(row, 8, sell_btn)
        
        self.update_stats()
    
    def sell_dialog(self, transaction_id):
        dialog = QDialog(self)
        dialog.setWindowTitle('بيع السهم')
        dialog.setGeometry(200, 200, 300, 150)
        
        layout = QVBoxLayout()
        
        price_label = QLabel('سعر البيع:')
        price_input = QDoubleSpinBox()
        price_input.setMaximum(1000000)
        
        sell_btn = QPushButton('بيع أكيد')
        sell_btn.clicked.connect(lambda: self.confirm_sell(transaction_id, price_input.value(), dialog))
        
        layout.addWidget(price_label)
        layout.addWidget(price_input)
        layout.addWidget(sell_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def confirm_sell(self, transaction_id, sell_price, dialog):
        if sell_price <= 0:
            QMessageBox.warning(self, 'تحذير', 'أدخل سعر بيع صحيح')
            return
        
        self.db.close_transaction(transaction_id, sell_price)
        dialog.close()
        self.load_transactions()
        QMessageBox.information(self, 'نجاح', 'تم بيع السهم بنجاح')
    
    def update_stats(self):
        transactions = self.db.get_all_transactions()
        calculator = PortfolioCalculator(transactions)
        
        total_invested = calculator.get_total_invested()
        current_value = calculator.get_total_current_value()
        profit_loss = calculator.get_total_profit_loss()
        profit_loss_percent = calculator.get_total_profit_loss_percentage()
        
        self.total_invested_label.setText(f'إجمالي المستثمر: {total_invested:.2f}')
        self.current_value_label.setText(f'القيمة الحالية: {current_value:.2f}')
        self.profit_loss_label.setText(f'الربح/الخسارة: {profit_loss:.2f}')
        self.profit_loss_percent_label.setText(f'النسبة: {profit_loss_percent:.2f}%')
    
    def closeEvent(self, event):
        self.db.close_database()
        event.accept()
