from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,  QTableWidgetItem, QAbstractItemView, \
    QSpacerItem, QSizePolicy, QPushButton, QHeaderView, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from DB_offline.queryes import delete_playbook

__all__ = ['DialogOpenPlaybook']


class DialogOpenPlaybook(QDialog):
    def __init__(self, playbook_info: list[tuple, ...],  parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Выбор плейбука')
        self.setFixedSize(600, 400)
        # self.setMinimumWidth(600)

        font = QFont()
        font.setPointSize(10)

        font.setBold(False)
        button_ok = QPushButton('ОК', parent=self)
        button_ok.setFont(font)
        button_ok.setFixedSize(100, 25)
        button_ok.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        button_cancel = QPushButton('Отмена', parent=self)
        button_cancel.setFont(font)
        button_cancel.setFixedSize(100, 25)
        button_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        button_delete = QPushButton('Удалить', parent=self)
        button_delete.setFont(font)
        button_delete.setFixedSize(100, 25)
        button_delete.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.table_playbooks = QTableWidget(len(playbook_info), 5)
        self.table_playbooks.setFont(font)
        self.table_playbooks.setHorizontalHeaderLabels(['id', 'Название плейбука', 'Тип плейбука', 'Дата обновления', 'Дата создания'])
        self.table_playbooks.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.table_playbooks.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table_playbooks.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_playbooks.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_playbooks.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table_playbooks.horizontalHeader().setSectionsClickable(False)
        font.setBold(True)
        self.table_playbooks.horizontalHeader().setFont(font)
        self.table_playbooks.verticalHeader().hide()
        self.table_playbooks.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_playbooks.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_playbooks.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table_playbooks.setShowGrid(False)
        self.table_playbooks.setCornerButtonEnabled(False)
        self.table_playbooks.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_playbooks.hideColumn(0)
        for i, playbook in enumerate(playbook_info):
            item = QTableWidgetItem(str(playbook[0]))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.table_playbooks.setItem(i, 0, item)

            item = QTableWidgetItem(playbook[1])
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.table_playbooks.setItem(i, 1, item)

            item = QTableWidgetItem(playbook[2])
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.table_playbooks.setItem(i, 2, item)

            item = QTableWidgetItem(playbook[3])
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.table_playbooks.setItem(i, 3, item)

            item = QTableWidgetItem(playbook[4])
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.table_playbooks.setItem(i, 4, item)
        # self.table_playbooks.sortItems(0, Qt.SortOrder.DescendingOrder)
        self.table_playbooks.itemDoubleClicked.connect(self.item_double_clicked)

        horizontal_layout_buttons = QHBoxLayout()
        horizontal_layout_buttons.addWidget(button_delete)
        horizontal_layout_buttons.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Fixed))
        horizontal_layout_buttons.addWidget(button_ok)
        horizontal_layout_buttons.addWidget(button_cancel)
        # horizontal_layout_buttons.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(self.table_playbooks)
        vertical_layout.addLayout(horizontal_layout_buttons)
        vertical_layout.addLayout(horizontal_layout_buttons)

        # self.table_playbooks.setFocus()
        self.table_playbooks.setCurrentCell(0, 1)

        button_ok.clicked.connect(self.accept)
        button_cancel.clicked.connect(self.reject)
        button_delete.clicked.connect(self.delete_playbook)

    def item_double_clicked(self):
        self.accept()

    def delete_playbook(self):
        playbook_id = self.table_playbooks.item(self.table_playbooks.currentRow(), 0).text()
        playbook_name = self.table_playbooks.item(self.table_playbooks.currentRow(), 1).text()
        question_dialog_save_current_playbook_online = QMessageBox(QMessageBox.Question, 'Удаление', f'Вы уверены что хотите удалить плейбук: {playbook_name}?', parent=self)
        question_dialog_save_current_playbook_online.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
        question_dialog_save_current_playbook_online.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
        question_dialog_save_current_playbook_online.exec()
        if not question_dialog_save_current_playbook_online.result():
            self.table_playbooks.removeRow(self.table_playbooks.currentRow())
            delete_playbook(int(playbook_id))

