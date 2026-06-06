from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QMessageBox,
    QSpinBox, QDoubleSpinBox, QFrame, QGraphicsOpacityEffect, QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont
from database import Database
from calculator import PortfolioCalculator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle('Stock Portfolio Manager')
        self.setGeometry(100, 100, 1360, 780)
        self.setMinimumSize(1120, 720)
        self.setStyleSheet(self.get_stylesheet())

        self.init_ui()
        self.run_intro_animation()

    def get_stylesheet(self):
        return """
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #020617, stop:0.45 #091825, stop:1 #111827);
            }
            QLabel#mainTitle {
                color: #f8fafc;
                font-size: 30px;
                font-weight: 800;
            }
            QLabel#subtitle {
                color: #cbd5e1;
                font-size: 14px;
            }
            QLabel#cardTitle {
                color: #94a3b8;
                font-size: 12px;
            }
            QLabel#cardValue {
                color: #ffffff;
                font-size: 24px;
                font-weight: 700;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: rgba(15, 23, 42, 0.85);
                border: 1px solid #334155;
                border-radius: 14px;
                color: #e2e8f0;
                min-height: 40px;
                padding: 0 12px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #60a5fa;
            }
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #2563eb);
                color: #ffffff;
                border: none;
                border-radius: 16px;
                min-height: 44px;
                padding: 0 22px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4338ca, stop:1 #1d4ed8);
            }
            QPushButton#secondaryButton {
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid #334155;
                color: #cbd5e1;
            }
            QPushButton#secondaryButton:hover {
                background: rgba(30, 41, 59, 0.95);
            }
            QPushButton:disabled {
                background-color: #334155;
                color: #94a3b8;
            }
            QTableWidget {
                background-color: rgba(15, 23, 42, 0.95);
                color: #e2e8f0;
                border: 1px solid rgba(148, 163, 184, 0.18);
                gridline-color: rgba(148, 163, 184, 0.12);
                border-radius: 18px;
            }
            QTableWidget::item {
                padding: 12px;
            }
            QHeaderView::section {
                background-color: rgba(15, 23, 42, 0.95);
                color: #f8fafc;
                border: none;
                padding: 10px;
                font-size: 12px;
                font-weight: 700;
            }
            QTableWidget::item:selected {
                background-color: rgba(37, 99, 235, 0.25);
                color: #ffffff;
            }
            QFrame#panelCard {
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 24px;
            }
            QFrame#topCard {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(56, 189, 248, 0.18), stop:1 rgba(139, 92, 246, 0.18));
                border: 1px solid rgba(56, 189, 248, 0.16);
                border-radius: 26px;
            }
            QFrame#infoCard {
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 20px;
            }
        """

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        hero_section = QFrame()
        hero_section.setObjectName('topCard')
        hero_layout = QHBoxLayout(hero_section)
        hero_layout.setContentsMargins(30, 24, 30, 24)
        hero_layout.setSpacing(30)

        hero_text = QVBoxLayout()
        self.title_label = QLabel('Stock Portfolio Manager')
        self.title_label.setObjectName('mainTitle')
        self.title_label.setFont(QFont('Segoe UI', 28, QFont.Black))
        hero_text.addWidget(self.title_label)

        subtitle = QLabel('واجهة احترافية لإدارة محفظتك وتصفّح صفقاتك بأشكال مرنة وفاخرة.')
        subtitle.setObjectName('subtitle')
        hero_text.addWidget(subtitle)

        hero_buttons = QHBoxLayout()
        hero_buttons.setSpacing(12)
        self.hero_add_transaction_btn = QPushButton('إضافة معاملة جديدة')
        self.hero_add_transaction_btn.clicked.connect(self.add_transaction)
        self.hero_add_transaction_btn.setObjectName('primaryButton')

        self.refresh_btn = QPushButton('تحديث البيانات')
        self.refresh_btn.setObjectName('secondaryButton')
        self.refresh_btn.clicked.connect(self.load_transactions)

        self.hero_add_transaction_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.hero_add_transaction_btn.setMinimumWidth(150)
        self.refresh_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.refresh_btn.setMinimumWidth(150)
        hero_buttons.addWidget(self.hero_add_transaction_btn)
        hero_buttons.addWidget(self.refresh_btn)
        hero_buttons.addStretch()
        hero_text.addLayout(hero_buttons)
        hero_text.addStretch()

        hero_layout.addLayout(hero_text, 3)

        hero_stats = QHBoxLayout()
        hero_stats.setSpacing(18)
        self.card_capital = self.create_dashboard_card('رأس المال الأساسي', '0', '#38bdf8')
        self.card_available = self.create_dashboard_card('النقد المتاح', '0', '#f59e0b')
        self.card_profit = self.create_dashboard_card('الربح/الخسارة', '0', '#f97316')
        hero_stats.addWidget(self.card_capital)
        hero_stats.addWidget(self.card_available)
        hero_stats.addWidget(self.card_profit)
        hero_layout.addLayout(hero_stats, 5)

        main_layout.addWidget(hero_section)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)

        left_panel = QVBoxLayout()
        left_panel.setSpacing(18)

        table_frame = QFrame()
        table_frame.setObjectName('panelCard')
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setSpacing(16)

        table_header = QLabel('سجل الصفقات')
        table_header.setFont(QFont('Segoe UI', 16, QFont.Bold))
        table_header.setStyleSheet('color: #ffffff;')
        table_layout.addWidget(table_header)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            'ID', 'اسم السهم', 'الكمية', 'سعر الشراء', 'سعر البيع',
            'الحالة', 'الربح/الخسارة', 'النسبة %', 'إجراء'
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setStyleSheet('QTableWidget { background: transparent; }')
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 130)
        self.table.setColumnWidth(4, 130)
        self.table.setColumnWidth(5, 110)
        self.table.setColumnWidth(6, 150)
        self.table.setColumnWidth(7, 110)
        self.table.setColumnWidth(8, 120)
        self.table.setMinimumHeight(430)

        table_layout.addWidget(self.table)
        left_panel.addWidget(table_frame)

        content_layout.addLayout(left_panel, 3)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(18)

        capital_frame = QFrame()
        capital_frame.setObjectName('panelCard')
        capital_layout = QHBoxLayout(capital_frame)
        capital_layout.setContentsMargins(18, 18, 18, 18)
        capital_layout.setSpacing(12)

        capital_label = QLabel('رأس المال الكلي')
        capital_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
        capital_label.setStyleSheet('color: #ffffff;')

        self.capital_input = QDoubleSpinBox()
        self.capital_input.setMaximum(1000000000)
        self.capital_input.setDecimals(2)
        self.capital_input.setPrefix('$ ')
        capital_start = self.db.get_capital() or 1000.00
        self.capital_input.setValue(capital_start)
        self.capital_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.capital_input.setMinimumWidth(160)
        self.capital_input.valueChanged.connect(self.on_capital_changed)

        capital_layout.addWidget(capital_label)
        capital_layout.addWidget(self.capital_input)
        right_panel.addWidget(capital_frame)

        action_frame = QFrame()
        action_frame.setObjectName('panelCard')
        action_layout = QVBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 20, 20, 20)
        action_layout.setSpacing(18)

        action_title = QLabel('أضف معاملة')
        action_title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        action_title.setStyleSheet('color: #ffffff;')
        action_layout.addWidget(action_title)

        field_layout = QVBoxLayout()
        field_layout.setSpacing(12)

        self.stock_name_input = self.create_labeled_input('اسم السهم', 'AAPL')
        self.quantity_input = self.create_labeled_spin('الكمية', 100)
        self.buy_price_input = self.create_labeled_double_spin('سعر الشراء', 20.5)
        self.sell_price_input = self.create_labeled_double_spin('سعر الخروج (اختياري)', 0.0)
        self.sell_price_input.findChild(QDoubleSpinBox).setMinimum(0)
        self.sell_price_input.findChild(QDoubleSpinBox).setSpecialValueText('غير محدد')

        field_layout.addWidget(self.stock_name_input)
        field_layout.addWidget(self.quantity_input)
        field_layout.addWidget(self.buy_price_input)
        field_layout.addWidget(self.sell_price_input)

        action_layout.addLayout(field_layout)
        self.add_transaction_btn = QPushButton('أضف الصفقة الآن')
        self.add_transaction_btn.clicked.connect(self.add_transaction)
        self.add_transaction_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_transaction_btn.setMinimumHeight(46)
        action_layout.addWidget(self.add_transaction_btn)

        right_panel.addWidget(action_frame)
        right_panel.addStretch()

        content_layout.addLayout(right_panel, 1)
        main_layout.addLayout(content_layout)

        main_widget.setLayout(main_layout)
        self.load_transactions()

    def create_dashboard_card(self, title, value, accent_color):
        card = QFrame()
        card.setObjectName('infoCard')
        card.setFixedHeight(140)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName('cardTitle')
        title_label.setFont(QFont('Segoe UI', 11, QFont.Medium))
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setObjectName('cardValue')
        value_label.setFont(QFont('Segoe UI', 22, QFont.Black))
        value_label.setStyleSheet(f'color: {accent_color};')
        layout.addWidget(value_label)

        return card

    def create_labeled_input(self, label_text, placeholder):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(label_text)
        label.setStyleSheet('color: #94a3b8;')
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        layout.addWidget(label)
        layout.addWidget(edit)
        return container

    def create_labeled_spin(self, label_text, default_value):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(label_text)
        label.setStyleSheet('color: #94a3b8;')
        spin = QSpinBox()
        spin.setMaximum(1000000)
        spin.setValue(default_value)
        layout.addWidget(label)
        layout.addWidget(spin)
        return container

    def create_labeled_double_spin(self, label_text, default_value):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(label_text)
        label.setStyleSheet('color: #94a3b8;')
        spin = QDoubleSpinBox()
        spin.setMaximum(1000000)
        spin.setValue(default_value)
        layout.addWidget(label)
        layout.addWidget(spin)
        return container

    def apply_fade(self, widget, delay=0):
        opacity = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity)
        animation = QPropertyAnimation(opacity, b'opacity')
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setDuration(650)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        QTimer.singleShot(delay, animation.start)
        return animation

    def run_intro_animation(self):
        self.animations = []
        self.animations.append(self.apply_fade(self.title_label, 0))
        self.animations.append(self.apply_fade(self.card_capital, 120))
        self.animations.append(self.apply_fade(self.card_available, 220))
        self.animations.append(self.apply_fade(self.card_profit, 320))
        self.animations.append(self.apply_fade(self.hero_add_transaction_btn, 420))
        self.animations.append(self.apply_fade(self.refresh_btn, 520))
        self.animations.append(self.apply_fade(self.add_transaction_btn, 620))

    def on_capital_changed(self, value):
        self.db.set_capital(value)
        self.update_stats()

    def add_transaction(self):
        stock_name = self.stock_name_input.findChild(QLineEdit).text().strip()
        quantity = self.quantity_input.findChild(QSpinBox).value()
        buy_price = self.buy_price_input.findChild(QDoubleSpinBox).value()
        sell_price_widget = self.sell_price_input.findChild(QDoubleSpinBox)
        sell_price = sell_price_widget.value() if sell_price_widget.value() > 0 else None

        if not stock_name or quantity <= 0 or buy_price <= 0:
            QMessageBox.warning(self, 'تحذير', 'أدخل بيانات صحيحة')
            return

        total_cost = quantity * buy_price
        available_cash = self.get_available_cash()

        if total_cost > available_cash:
            QMessageBox.warning(
                self,
                'رأس المال غير كافٍ',
                f'لا يوجد نقد كافٍ لهذه الصفقة. النقد المتاح حاليًا: {available_cash:.2f}'
            )
            return

        self.db.add_transaction(stock_name, quantity, buy_price, sell_price)
        self.stock_name_input.findChild(QLineEdit).clear()
        self.quantity_input.findChild(QSpinBox).setValue(0)
        self.buy_price_input.findChild(QDoubleSpinBox).setValue(0)
        sell_price_widget.setValue(0)

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
            self.table.setItem(row, 4, QTableWidgetItem(f'{sell_price:.2f}' if sell_price else '-'))
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

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(6)

            sell_btn = QPushButton('بيع')
            sell_btn.setObjectName('secondaryButton')
            sell_btn.setEnabled(status == 'open')
            sell_btn.clicked.connect(lambda checked, tid=transaction_id: self.sell_dialog(tid))
            action_layout.addWidget(sell_btn)

            delete_btn = QPushButton('حذف')
            delete_btn.setObjectName('secondaryButton')
            delete_btn.clicked.connect(lambda checked, tid=transaction_id: self.delete_transaction(tid))
            action_layout.addWidget(delete_btn)

            self.table.setCellWidget(row, 8, action_widget)

        self.update_stats()

    def sell_dialog(self, transaction_id):
        dialog = QDialog(self)
        dialog.setWindowTitle('بيع السهم')
        dialog.setModal(True)
        dialog.setFixedSize(360, 190)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        price_label = QLabel('سعر البيع:')
        price_input = QDoubleSpinBox()
        price_input.setMaximum(1000000)

        sell_btn = QPushButton('بيع أكيد')
        sell_btn.clicked.connect(lambda: self.confirm_sell(transaction_id, price_input.value(), dialog))

        layout.addWidget(price_label)
        layout.addWidget(price_input)
        layout.addWidget(sell_btn)

        dialog.exec_()

    def confirm_sell(self, transaction_id, sell_price, dialog):
        if sell_price <= 0:
            QMessageBox.warning(self, 'تحذير', 'أدخل سعر بيع صحيح')
            return

        self.db.close_transaction(transaction_id, sell_price)
        dialog.close()
        self.load_transactions()
        QMessageBox.information(self, 'نجاح', 'تم بيع السهم بنجاح')

    def delete_transaction(self, transaction_id):
        confirm = QMessageBox.question(
            self,
            'تأكيد الحذف',
            'هل تريد حذف هذه الصفقة من المحفظة؟',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_transaction(transaction_id)
            self.load_transactions()
            QMessageBox.information(self, 'تم', 'تم حذف الصفقة بنجاح')

    def update_stats(self):
        transactions = self.db.get_all_transactions()
        calculator = PortfolioCalculator(transactions)

        total_capital = self.db.get_capital()
        reserved_capital = calculator.get_total_open_invested()
        available_cash = max(total_capital - reserved_capital, 0)
        profit_loss = calculator.get_total_profit_loss()

        self.card_capital.findChild(QLabel, 'cardValue').setText(f'{total_capital:.2f}')
        self.card_available.findChild(QLabel, 'cardValue').setText(f'{available_cash:.2f}')
        self.card_profit.findChild(QLabel, 'cardValue').setText(f'{profit_loss:.2f}')

    def get_available_cash(self):
        total_capital = self.db.get_capital()
        transactions = self.db.get_all_transactions()
        calculator = PortfolioCalculator(transactions)
        reserved_capital = calculator.get_total_open_invested()
        return max(total_capital - reserved_capital, 0)

    def closeEvent(self, event):
        self.db.close_database()
        event.accept()
