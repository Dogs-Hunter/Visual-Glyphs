import sys
import os
import json
import subprocess
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QDialog,
    QLineEdit, QTextEdit, QFormLayout, QMessageBox, QHeaderView, QLabel, QFrame,
    QSpinBox, QCheckBox, QGroupBox, QSlider, QFileDialog, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont

FILENAME_DEFAULT = "passwords.json"
SETTINGS_FILE = "settings.json"


# 🎨 Стабильная тема
def get_modern_style(font_size=13):
    return f"""
QWidget {{ background-color: transparent; color: #e2e8f0; font-family: "Segoe UI", "Roboto", "Arial", sans-serif; font-size: {font_size}px; }}
QMainWindow {{ background-color: #2a2a32; border: 2px solid #454552; border-radius: 14px; }}
QDialog {{ background-color: #2a2a32; border: 2px solid #454552; }}
QFrame#mainContainer {{ background-color: #25252e; border: 2px solid #454552; border-radius: 14px; }}
QFrame#titleBar {{ background-color: #2a2a32; border-top-left-radius: 12px; border-top-right-radius: 12px; }}
QLabel#windowTitle {{ color: #f8fafc; font-weight: 600; font-size: {font_size + 1}px; background: transparent; }}

QPushButton#titleBtn {{ background: transparent; border: none; border-radius: 4px; color: #94a3b8; font-size: {font_size + 3}px; padding: 4px 8px; min-width: 24px; max-width: 24px; }}
QPushButton#titleBtn:hover {{ background-color: #3a3a45; color: #ffffff; }}
QPushButton#titleBtn#closeBtn:hover {{ background-color: #ef4444; color: #ffffff; }}

QLineEdit, QTextEdit {{ background-color: #32323b; border: 1px solid #454552; border-radius: 8px; padding: 8px 12px; color: #f1f5f9; selection-background-color: #2563eb; selection-color: #ffffff; }}
QLineEdit:focus, QTextEdit:focus {{ border-color: #60a5fa; background-color: #383842; }}
QLabel {{ background-color: transparent; color: #cbd5e1; font-weight: 500; }}

QPushButton {{ background-color: #32323b; border: 1px solid #454552; border-radius: 8px; padding: 8px 16px; color: #ffffff; font-weight: 500; }}
QPushButton:hover {{ background-color: #3d3d48; border-color: #52525b; }}
QPushButton:pressed {{ background-color: #2d2d35; }}
QPushButton:disabled {{ opacity: 0.5; }}
QPushButton#addBtn {{ background-color: #10b981; border-color: #059669; }}
QPushButton#addBtn:hover {{ background-color: #059669; }}
QPushButton#editBtn {{ background-color: #3b82f6; border-color: #2563eb; }}
QPushButton#editBtn:hover {{ background-color: #2563eb; }}
QPushButton#deleteBtn {{ background-color: #ef4444; border-color: #dc2626; }}
QPushButton#deleteBtn:hover {{ background-color: #dc2626; }}
QPushButton#settingsBtn {{ background-color: #8b5cf6; border-color: #7c3aed; }}
QPushButton#settingsBtn:hover {{ background-color: #7c3aed; }}
QPushButton#exportBtn {{ background-color: #06b6d4; border-color: #0891b2; }}
QPushButton#exportBtn:hover {{ background-color: #0891b2; }}
QPushButton#importBtn {{ background-color: #f59e0b; border-color: #d97706; }}
QPushButton#importBtn:hover {{ background-color: #d97706; }}
QPushButton#copyBtn {{ padding: 4px 8px; font-size: {font_size - 1}px; min-width: 28px; max-width: 28px; background-color: #32323b; border: 1px solid #454552; border-radius: 6px; }}
QPushButton#copyBtn:hover {{ background-color: #3d3d48; border-color: #52525b; }}

QTableWidget {{ background-color: #25252e; gridline-color: #35353e; border: 1px solid #35353e; border-radius: 10px; alternate-background-color: #2d2d35; outline: none; selection-background-color: #2563eb; selection-color: #ffffff; }}
QTableWidget::item {{ padding: 8px 8px; border: none; }}
QTableWidget::item:selected {{ background-color: #5a7ca5; color: #f8fafc; border: none; }}
QTableWidget::item:selected:!active {{ background-color: #3d3d48; color: #cbd5e1; border: none; }}
QHeaderView::section {{ background-color: #2a2a32; padding: 10px; border: none; border-bottom: 2px solid #454552; color: #94a3b8; font-weight: 600; font-size: {font_size}px; }}
QTableWidget QTableCornerButton::section {{ background-color: #2a2a32; border: none; border-bottom: 2px solid #454552; }}

QGroupBox {{ border: 1px solid #454552; border-radius: 8px; margin-top: 14px; padding-top: 12px; font-weight: 600; color: #f8fafc; }}
QSlider::groove:horizontal {{ border: 1px solid #454552; height: 6px; background: #32323b; border-radius: 3px; }}
QSlider::handle:horizontal {{ background: #3b82f6; border: 1px solid #2563eb; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }}
QSlider::handle:horizontal:hover {{ background: #60a5fa; border-color: #3b82f6; }}
QSpinBox {{ background-color: #32323b; border: 1px solid #454552; border-radius: 6px; padding: 4px 8px; color: #f1f5f9; min-width: 80px; }}
QSpinBox:focus {{ border-color: #60a5fa; }}
QCheckBox {{ spacing: 8px; color: #cbd5e1; }}
QCheckBox::indicator {{ width: 18px; height: 18px; border: 1px solid #454552; border-radius: 4px; background-color: #32323b; }}
QCheckBox::indicator:checked {{ background-color: #10b981; border-color: #059669; }}
QCheckBox::indicator:hover {{ border-color: #52525b; }}
"""


class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Настройки")
        self.setFixedSize(520, 620)

        self.setStyleSheet("""
            QDialog { background-color: #2a2a32; border: 2px solid #454552; }
            QLabel { color: #cbd5e1; }
            QLineEdit, QSpinBox { background-color: #32323b; border: 1px solid #454552; border-radius: 6px; padding: 6px; color: #f1f5f9; }
            QPushButton { background-color: #32323b; border: 1px solid #454552; border-radius: 8px; padding: 8px 16px; color: #fff; }
            QPushButton:hover { background-color: #3d3d48; }
            QPushButton#addBtn { background-color: #10b981; border-color: #059669; }
            QPushButton#addBtn:hover { background-color: #059669; }
            QGroupBox { border: 1px solid #454552; border-radius: 8px; margin-top: 14px; padding-top: 12px; font-weight: 600; color: #f8fafc; }
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { background: #25252e; width: 10px; border-radius: 5px; margin: 0px; }
            QScrollBar::handle:vertical { background: #454552; border-radius: 5px; min-height: 30px; }
            QScrollBar::handle:vertical:hover { background: #52525b; }
            QScrollBar::add-line, QScrollBar::sub-line { height: 0; border: none; background: none; }
            QScrollBar::add-page, QScrollBar::sub-page { background: none; }
        """)

        self.settings = settings or self.get_default_settings()
        self.setup_ui()

    def get_default_settings(self):
        return {
            "font_size": 13, "auto_clear_clipboard": True, "clear_clipboard_seconds": 30,
            "show_passwords": False, "confirm_delete": True, "always_on_top": False,
            "remember_window_pos": True, "auto_save": True,
            "base_dir": os.getcwd(),
            "json_filename": "passwords.json",
            "png_filename": "passwords_backup.png",
            "encryption_key": ""
        }

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(14)

        title_label = QLabel("⚙️ Настройки приложения")
        title_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #f8fafc;")
        content_layout.addWidget(title_label)

        interface_group = QGroupBox("Интерфейс")
        interface_layout = QVBoxLayout()
        interface_layout.setSpacing(8)

        font_row = QHBoxLayout()
        font_label = QLabel("Размер шрифта:")
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setRange(10, 18)
        self.font_slider.setValue(self.settings["font_size"])
        self.font_slider.setTickPosition(QSlider.TicksBelow)
        self.font_slider.setTickInterval(1)
        self.font_size_label = QLabel(f"{self.settings['font_size']}px")
        self.font_size_label.setFixedWidth(35)
        self.font_slider.valueChanged.connect(lambda v: self.font_size_label.setText(f"{v}px"))

        font_row.addWidget(font_label)
        font_row.addWidget(self.font_slider)
        font_row.addWidget(self.font_size_label)
        interface_layout.addLayout(font_row)

        self.show_passwords_cb = QCheckBox("Показывать пароли в таблице (иначе •••••)")
        self.show_passwords_cb.setChecked(self.settings["show_passwords"])
        interface_layout.addWidget(self.show_passwords_cb)

        self.always_on_top_cb = QCheckBox("Окно всегда поверх других")
        self.always_on_top_cb.setChecked(self.settings["always_on_top"])
        interface_layout.addWidget(self.always_on_top_cb)
        interface_group.setLayout(interface_layout)
        content_layout.addWidget(interface_group)

        storage_group = QGroupBox("Хранение данных")
        storage_layout = QVBoxLayout()
        storage_layout.setSpacing(8)

        path_row = QHBoxLayout()
        self.base_path_edit = QLineEdit(self.settings["base_dir"])
        self.base_path_edit.setReadOnly(True)
        self.path_btn = QPushButton("📁 Выбрать")
        self.path_btn.setFixedWidth(90)
        self.path_btn.clicked.connect(self.browse_folder)
        path_row.addWidget(QLabel("Папка:"))
        path_row.addWidget(self.base_path_edit)
        path_row.addWidget(self.path_btn)
        storage_layout.addLayout(path_row)

        self.json_name_edit = QLineEdit(self.settings["json_filename"])
        self.json_name_edit.setPlaceholderText("passwords.json")
        storage_layout.addWidget(QLabel("Имя JSON:"))
        storage_layout.addWidget(self.json_name_edit)

        self.png_name_edit = QLineEdit(self.settings["png_filename"])
        self.png_name_edit.setPlaceholderText("passwords_backup.png")
        storage_layout.addWidget(QLabel("Имя PNG:"))
        storage_layout.addWidget(self.png_name_edit)
        storage_group.setLayout(storage_layout)
        content_layout.addWidget(storage_group)

        security_group = QGroupBox("Безопасность")
        security_layout = QVBoxLayout()
        security_layout.setSpacing(8)

        key_row = QHBoxLayout()
        self.encryption_key_edit = QLineEdit(self.settings["encryption_key"])
        self.encryption_key_edit.setPlaceholderText("Введите пароль шифрования")
        self.encryption_key_edit.setToolTip("Пароль передаётся напрямую в скрипт через аргумент -p")
        key_row.addWidget(QLabel("Пароль:"))
        key_row.addWidget(self.encryption_key_edit)
        security_layout.addLayout(key_row)

        self.auto_clear_cb = QCheckBox("Автоочистка буфера обмена через")
        self.auto_clear_cb.setChecked(self.settings["auto_clear_clipboard"])
        security_layout.addWidget(self.auto_clear_cb)

        clear_time_layout = QHBoxLayout()
        self.clear_seconds_spin = QSpinBox()
        self.clear_seconds_spin.setRange(5, 300)
        self.clear_seconds_spin.setSingleStep(5)
        self.clear_seconds_spin.setValue(self.settings["clear_clipboard_seconds"])
        self.clear_seconds_spin.setEnabled(self.settings["auto_clear_clipboard"])
        self.clear_seconds_spin.setSuffix(" сек")
        self.clear_seconds_spin.setFixedWidth(110)
        self.auto_clear_cb.toggled.connect(self.clear_seconds_spin.setEnabled)
        clear_time_layout.addSpacing(24)
        clear_time_layout.addWidget(self.clear_seconds_spin)
        clear_time_layout.addStretch()
        security_layout.addLayout(clear_time_layout)

        self.confirm_delete_cb = QCheckBox("Подтверждение при удалении")
        self.confirm_delete_cb.setChecked(self.settings["confirm_delete"])
        security_layout.addWidget(self.confirm_delete_cb)
        security_group.setLayout(security_layout)
        content_layout.addWidget(security_group)

        save_group = QGroupBox("Сохранение")
        save_layout = QVBoxLayout()
        save_layout.setSpacing(8)
        self.auto_save_cb = QCheckBox("Автосохранение при изменениях")
        self.auto_save_cb.setChecked(self.settings["auto_save"])
        save_layout.addWidget(self.auto_save_cb)
        self.remember_pos_cb = QCheckBox("Запоминать положение и размер окна")
        self.remember_pos_cb.setChecked(self.settings["remember_window_pos"])
        save_layout.addWidget(self.remember_pos_cb)
        save_group.setLayout(save_layout)
        content_layout.addWidget(save_group)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        reset_btn = QPushButton("🔄 Сбросить")
        reset_btn.clicked.connect(self.reset_to_defaults)
        cancel_btn = QPushButton("✖ Отмена")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("💾 Сохранить")
        save_btn.setObjectName("addBtn")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        content_layout.addLayout(btn_layout)
        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def browse_folder(self):
        options = QFileDialog.Options(QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку", self.base_path_edit.text(), options=options)
        if folder:
            self.base_path_edit.setText(folder)

    def reset_to_defaults(self):
        defaults = self.get_default_settings()
        self.font_slider.setValue(defaults["font_size"])
        self.show_passwords_cb.setChecked(defaults["show_passwords"])
        self.always_on_top_cb.setChecked(defaults["always_on_top"])
        self.auto_clear_cb.setChecked(defaults["auto_clear_clipboard"])
        self.clear_seconds_spin.setValue(defaults["clear_clipboard_seconds"])
        self.confirm_delete_cb.setChecked(defaults["confirm_delete"])
        self.auto_save_cb.setChecked(defaults["auto_save"])
        self.remember_pos_cb.setChecked(defaults["remember_window_pos"])
        self.base_path_edit.setText(defaults["base_dir"])
        self.json_name_edit.setText(defaults["json_filename"])
        self.png_name_edit.setText(defaults["png_filename"])
        self.encryption_key_edit.setText("")

    def save_settings(self):
        self.settings.update({
            "font_size": self.font_slider.value(),
            "show_passwords": self.show_passwords_cb.isChecked(),
            "always_on_top": self.always_on_top_cb.isChecked(),
            "auto_clear_clipboard": self.auto_clear_cb.isChecked(),
            "clear_clipboard_seconds": self.clear_seconds_spin.value(),
            "confirm_delete": self.confirm_delete_cb.isChecked(),
            "auto_save": self.auto_save_cb.isChecked(),
            "remember_window_pos": self.remember_pos_cb.isChecked(),
            "base_dir": self.base_path_edit.text().strip(),
            "json_filename": self.json_name_edit.text().strip(),
            "png_filename": self.png_name_edit.text().strip(),
            "encryption_key": self.encryption_key_edit.text()
        })
        self.save_to_file()
        self.accept()

    def save_to_file(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить настройки:\n{e}")

    def get_settings(self):
        return self.settings


class RecordDialog(QDialog):
    def __init__(self, parent=None, record=None, show_passwords=False):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.record = record
        self.show_passwords = show_passwords
        self.setWindowTitle("Новая запись" if record is None else "Редактирование")
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog { background-color: #2a2a32; border: 2px solid #454552; }
            QLabel { color: #cbd5e1; }
            QLineEdit, QTextEdit { background-color: #32323b; border: 1px solid #454552; border-radius: 8px; padding: 8px 12px; color: #f1f5f9; }
            QPushButton { background-color: #32323b; border: 1px solid #454552; border-radius: 8px; padding: 8px 16px; color: #fff; }
            QPushButton:hover { background-color: #3d3d48; }
            QPushButton#copyBtn { min-width: 28px; max-width: 28px; padding: 4px 8px; }
        """)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        form_layout = QFormLayout()
        form_layout.setSpacing(14)
        form_layout.setContentsMargins(0, 0, 0, 0)

        self.title_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        self.login_edit = QLineEdit()
        self.password_edit = QLineEdit()
        if not self.show_passwords:
            self.password_edit.setEchoMode(QLineEdit.Password)

        if self.record:
            self.title_edit.setText(str(self.record.get("title", "")))
            self.desc_edit.setPlainText(str(self.record.get("description", "")))
            self.login_edit.setText(str(self.record.get("login", "")))
            self.password_edit.setText(str(self.record.get("password", "")))

        def add_copy_field(layout, label_text, line_edit):
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.addWidget(line_edit)
            copy_btn = QPushButton("📋")
            copy_btn.setObjectName("copyBtn")
            copy_btn.setToolTip("Копировать в буфер обмена")
            copy_btn.clicked.connect(lambda: self.copy_to_clipboard(line_edit))
            row_layout.addWidget(copy_btn)
            layout.addRow(QLabel(label_text), row_layout)

        form_layout.addRow(QLabel("Заголовок"), self.title_edit)
        form_layout.addRow(QLabel("Описание"), self.desc_edit)
        add_copy_field(form_layout, "Логин", self.login_edit)
        add_copy_field(form_layout, "Пароль", self.password_edit)
        main_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        ok_btn = QPushButton("💾 Сохранить")
        cancel_btn = QPushButton("✖ Отмена")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        main_layout.addLayout(btn_layout)

    def copy_to_clipboard(self, widget):
        text = widget.text() if isinstance(widget, QLineEdit) else widget.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            widget.setStyleSheet("border-color: #10b981; background-color: #162a1d;")
            QTimer.singleShot(400, lambda: widget.setStyleSheet(""))
            parent_window = self.parent()
            if hasattr(parent_window, 'start_clipboard_timer'):
                parent_window.start_clipboard_timer()

    def get_data(self):
        return {
            "title": self.title_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
            "login": self.login_edit.text().strip(),
            "password": self.password_edit.text().strip()
        }


class PasswordNotepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Блокнот паролей")
        self.resize(900, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.records = []
        self.settings = self.load_settings()
        self.dragging = False
        self.drag_pos = QPoint()
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.clear_clipboard)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.base_dir = self.settings.get("base_dir", os.getcwd())
        self.json_path = os.path.join(self.base_dir, self.settings.get("json_filename", "passwords.json"))
        self.png_path = os.path.join(self.base_dir, self.settings.get("png_filename", "passwords_backup.png"))

        self.load_records()
        self.setup_ui()
        self.apply_settings()
        self.refresh_table()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return SettingsDialog().get_default_settings()

    def apply_settings(self):
        font_size = self.settings.get("font_size", 13)
        self.setStyleSheet(get_modern_style(font_size))
        self.update_clipboard_settings()

        if self.settings.get("always_on_top", False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()

        if self.settings.get("remember_window_pos", False) and "window_geometry" in self.settings:
            geom = self.settings["window_geometry"]
            self.setGeometry(geom["x"], geom["y"], geom["width"], geom["height"])

    def update_clipboard_settings(self):
        if self.settings.get("auto_clear_clipboard", True):
            self.clipboard_timer.setInterval(self.settings["clear_clipboard_seconds"] * 1000)
        else:
            self.clipboard_timer.stop()

    def start_clipboard_timer(self):
        if self.settings.get("auto_clear_clipboard", True):
            self.clipboard_timer.start()

    def setup_ui(self):
        container = QFrame()
        container.setObjectName("mainContainer")
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_bar = QFrame()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(36)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(12, 0, 8, 0)
        title_layout.setSpacing(10)

        title_label = QLabel("🔐 Блокнот паролей")
        title_label.setObjectName("windowTitle")
        title_label.mousePressEvent = lambda e: self._start_drag(e)
        title_label.mouseMoveEvent = lambda e: self._do_drag(e)
        title_label.mouseReleaseEvent = lambda e: self._end_drag(e)

        close_btn = QPushButton("✕")
        close_btn.setObjectName("titleBtn closeBtn")
        close_btn.setToolTip("Закрыть")
        close_btn.clicked.connect(self.close)

        min_btn = QPushButton("─")
        min_btn.setObjectName("titleBtn")
        min_btn.setToolTip("Свернуть")
        min_btn.clicked.connect(self.showMinimized)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(min_btn)
        title_layout.addWidget(close_btn)
        layout.addWidget(title_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Заголовок", "Логин", "Пароль", "Описание"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setWordWrap(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        action_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Добавить")
        self.add_btn.setObjectName("addBtn")
        self.edit_btn = QPushButton("✏️ Редактировать")
        self.edit_btn.setObjectName("editBtn")
        self.delete_btn = QPushButton("🗑️ Удалить")
        self.delete_btn.setObjectName("deleteBtn")
        for btn in [self.add_btn, self.edit_btn, self.delete_btn]:
            btn.setFixedHeight(40)

        action_layout.addWidget(self.add_btn)
        action_layout.addWidget(self.edit_btn)
        action_layout.addWidget(self.delete_btn)
        layout.addLayout(action_layout)

        io_layout = QHBoxLayout()
        self.export_btn = QPushButton("📤 Экспорт в PNG")
        self.export_btn.setObjectName("exportBtn")
        self.import_btn = QPushButton("📥 Импорт из PNG")
        self.import_btn.setObjectName("importBtn")
        self.settings_btn = QPushButton("⚙️ Настройки")
        self.settings_btn.setObjectName("settingsBtn")
        for btn in [self.export_btn, self.import_btn, self.settings_btn]:
            btn.setFixedHeight(40)

        io_layout.addWidget(self.export_btn)
        io_layout.addWidget(self.import_btn)
        io_layout.addStretch()
        io_layout.addWidget(self.settings_btn)
        layout.addLayout(io_layout)

        self.add_btn.clicked.connect(self.add_record)
        self.edit_btn.clicked.connect(self.edit_record)
        self.delete_btn.clicked.connect(self.delete_record)
        self.export_btn.clicked.connect(self.export_records)
        self.import_btn.clicked.connect(self.import_records)
        self.settings_btn.clicked.connect(self.open_settings)

    def open_settings(self):
        try:
            dialog = SettingsDialog(self, self.settings)
            if dialog.exec_() == QDialog.Accepted:
                old_font_size = self.settings.get("font_size", 13)
                self.settings = dialog.get_settings()
                self.save_settings()

                new_font_size = self.settings.get("font_size", 13)
                if old_font_size != new_font_size:
                    self.setStyleSheet(get_modern_style(new_font_size))

                self.base_dir = self.settings["base_dir"]
                self.json_path = os.path.join(self.base_dir, self.settings["json_filename"])
                self.refresh_table()

                if self.settings.get("always_on_top", False):
                    self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
                else:
                    self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
                self.show()

                self.update_clipboard_settings()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть/применить настройки:\n{str(e)}")

    def save_settings(self):
        if self.settings.get("remember_window_pos", False):
            self.settings["window_geometry"] = {
                "x": self.x(), "y": self.y(), "width": self.width(), "height": self.height()
            }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить настройки:\n{e}")

    def clear_clipboard(self):
        self.clipboard_timer.stop()
        QApplication.clipboard().clear()

    def _start_drag(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def _do_drag(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def _end_drag(self, event):
        self.dragging = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self._start_drag(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton: self._do_drag(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._end_drag(event)
        super().mouseReleaseEvent(event)

    def load_records(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.records = data.get("records", []) if isinstance(data, dict) else []
            except Exception as e:
                QMessageBox.warning(self, "Ошибка загрузки", f"Не удалось прочитать файл:\n{e}")
                self.records = []
        else:
            self.records = []

    def save_records(self):
        if not self.settings.get("auto_save", True): return
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump({"records": self.records}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", f"Не удалось сохранить файл:\n{e}")

    def get_next_id(self):
        # Надёжное получение следующего ID (игнорирует None/строки/отсутствующие поля)
        ids = [r.get("record_id") for r in self.records if isinstance(r.get("record_id"), int)]
        return (max(ids) + 1) if ids else 1

    def refresh_table(self):
        self.table.setRowCount(len(self.records))
        show_passwords = self.settings.get("show_passwords", False)
        for i, rec in enumerate(self.records):
            # Гарантируем корректное отображение ID
            rec_id = rec.get("record_id")
            id_val = int(rec_id) if isinstance(rec_id, (int, float)) else 0

            self.table.setItem(i, 0, QTableWidgetItem(str(id_val)))
            self.table.setItem(i, 1, QTableWidgetItem(str(rec.get("title", ""))))
            self.table.setItem(i, 2, QTableWidgetItem(str(rec.get("login", ""))))
            password = rec.get("password", "") if show_passwords else "•" * 8
            self.table.setItem(i, 3, QTableWidgetItem(password))
            self.table.setItem(i, 4, QTableWidgetItem(str(rec.get("description", ""))))
            self.table.item(i, 0).setTextAlignment(Qt.AlignCenter)
        QTimer.singleShot(0, self.table.resizeRowsToContents)

    def add_record(self):
        dialog = RecordDialog(self, show_passwords=self.settings.get("show_passwords", False))
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not any([data["title"], data["login"], data["password"]]):
                QMessageBox.warning(self, "Внимание", "Заполните хотя бы одно поле.")
                return
            new_record = {"record_id": self.get_next_id(), **data}
            self.records.append(new_record)
            self.save_records()
            self.refresh_table()

    def edit_record(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.information(self, "Внимание", "Выберите запись.")
            return
        record = self.records[row]
        dialog = RecordDialog(self, record=record, show_passwords=self.settings.get("show_passwords", False))
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.records[row].update(data)
            self.save_records()
            self.refresh_table()

    def delete_record(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.information(self, "Внимание", "Выберите запись.")
            return
        if self.settings.get("confirm_delete", True):
            title = self.records[row].get("title", "Без названия")
            if QMessageBox.question(self, "Подтверждение", f"Удалить <b>{title}</b>?") != QMessageBox.Yes:
                return
        self.records.pop(row)
        self.save_records()
        self.refresh_table()

    def _check_scripts(self, script_name):
        script_path = os.path.join(self.script_dir, script_name)
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "Ошибка", f"Файл {script_name} не найден в папке:\n{self.script_dir}")
            return None
        return script_path

    def export_records(self):
        script_path = self._check_scripts("to_image.py")
        if not script_path: return
        if not self.settings.get("encryption_key"):
            QMessageBox.warning(self, "Внимание", "Укажите пароль шифрования в настройках.")
            return

        tmp_json = os.path.join(self.base_dir, f"_tmp_export_{os.getpid()}.json")
        try:
            with open(tmp_json, "w", encoding="utf-8") as f:
                json.dump({"records": self.records}, f, ensure_ascii=False, indent=2)

            QApplication.setOverrideCursor(Qt.WaitCursor)
            cmd = [sys.executable, script_path, tmp_json, "-o", self.png_path, "-p", self.settings["encryption_key"]]
            subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True, cwd=self.script_dir)
            QMessageBox.information(self, "Успех", f"Записи успешно зашифрованы:\n{self.png_path}")
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip() or "Ошибка выполнения to_image.py"
            QMessageBox.critical(self, "Ошибка экспорта", err_msg)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            QApplication.restoreOverrideCursor()
            if os.path.exists(tmp_json): os.unlink(tmp_json)

    def import_records(self):
        script_path = self._check_scripts("from_image.py")
        if not script_path: return
        if not self.settings.get("encryption_key"):
            QMessageBox.warning(self, "Внимание", "Укажите пароль шифрования в настройках.")
            return
        if not os.path.exists(self.png_path):
            QMessageBox.warning(self, "Внимание", f"Файл {self.png_path} не найден.")
            return

        tmp_json = os.path.join(self.base_dir, f"_tmp_import_{os.getpid()}.json")
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            cmd = [sys.executable, script_path, self.png_path, "-o", tmp_json, "-p", self.settings["encryption_key"]]
            subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True, cwd=self.script_dir)

            with open(tmp_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                imported_records = data.get("records", [])

            # 🔧 Восстановление и валидация record_id
            next_id = 1
            fixed_records = []
            for rec in imported_records:
                rec_id = rec.get("record_id")
                # Если ID отсутствует, не целое число или <= 0 → генерируем новый
                if not isinstance(rec_id, int) or rec_id <= 0:
                    rec["record_id"] = next_id
                fixed_records.append(rec)
                # Поднимаем next_id выше текущего, чтобы избежать дубликатов
                next_id = max(next_id, rec["record_id"] + 1)

            if QMessageBox.question(self, "Подтверждение импорта",
                                    f"Найдено {len(fixed_records)} записей. Заменить текущие данные?") == QMessageBox.Yes:
                self.records = fixed_records
                self.save_records()
                self.refresh_table()
                QMessageBox.information(self, "Успех", "Записи успешно импортированы.")
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            if "InvalidTag" in err_msg or "неверный ключ" in err_msg:
                QMessageBox.critical(self, "Ошибка импорта (InvalidTag)",
                                     "🔐 Пароль не совпадает с тем, которым был зашифрован файл.\n\n"
                                     "Введите ТОЧНО ТУ ЖЕ СТРОКУ, что использовали при экспорте.")
            else:
                QMessageBox.critical(self, "Ошибка импорта", f"from_image.py завершился с ошибкой:\n{err_msg}")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка импорта", "Не удалось прочитать расшифрованный JSON.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            QApplication.restoreOverrideCursor()
            if os.path.exists(tmp_json): os.unlink(tmp_json)

    def closeEvent(self, event):
        if self.settings.get("remember_window_pos", False):
            self.save_settings()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    window = PasswordNotepad()
    window.show()
    sys.exit(app.exec_())