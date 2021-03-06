from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import Slot, Signal

class ExtractorWidget(QtWidgets.QWidget):
    def __init__(self, parent, extractor):
        super().__init__(parent=parent)
        self.extractor = extractor

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.create_word_lists())
        layout.addWidget(self.create_html_field())
        layout.addWidget(self.create_control_group())

        self.setLayout(layout)

    def create_html_field(self):
        group = QtWidgets.QGroupBox()
        group.setTitle("HTML")

        layout = QtWidgets.QVBoxLayout()

        self.html_field = QtWidgets.QTextEdit()
        self.html_field.setAlignment(QtCore.Qt.AlignLeft)
        self.html_field.textChanged.connect(self.text_changed)

        layout.addWidget(self.html_field)
        group.setLayout(layout)

        return group

    def text_changed(self):
        self.extractor.text = self.html_field.toPlainText()

    def create_control_group(self):
        group = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()

        save_button = QtWidgets.QPushButton()
        save_button.setText("Save")
        save_button.setToolTip("Save changes to dictionary file")
        save_button.clicked.connect(self.extractor.save_dictionary)

        load_button = QtWidgets.QPushButton()
        load_button.setText("Load")
        load_button.setToolTip("Load dictionary from file")
        load_button.clicked.connect(self.extractor.load_dictionary)

        extract_button = QtWidgets.QPushButton()
        extract_button.setText("Extract")
        extract_button.setToolTip("Extract the words to remove/add from html")
        extract_button.clicked.connect(self.extractor.get_dictionary_diff)

        apply_button = QtWidgets.QPushButton()
        apply_button.setText("Apply")
        apply_button.setToolTip("Apply changes to dictionary in memory (Use save to update dictionary on disk)")
        apply_button.clicked.connect(self.extractor.apply_dictionary_diff)

        layout.addWidget(save_button)
        layout.addWidget(load_button)
        layout.addWidget(extract_button)
        layout.addWidget(apply_button)

        group.setLayout(layout)

        # highlight save button if dictionary changed
        def on_dict_change(is_changed):
            font = QtGui.QFont()
            font.setBold(is_changed) 
            save_button.setFont(font)
            if not is_changed:
                save_button.setText("Save")
                save_button.setToolTip("Save changes to dictionary file")
            else:
                save_button.setText("Save*")
                save_button.setToolTip("Unsaved changes to dictionary")

        self.extractor.dictionary_changed.connect(on_dict_change)

        return group
    
    def create_word_lists(self):
        group = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(self.create_word_list("Trace list", self.extractor.trace_word_list))
        layout.addWidget(self.create_word_list("Extracted list", self.extractor.extracted_word_list))
        layout.addWidget(self.create_word_list("Add list", self.extractor.add_word_list))
        layout.addWidget(self.create_word_list("Removed list", self.extractor.removed_word_list))

        group.setLayout(layout)
        return group

    def create_word_list(self, title, model):
        group = QtWidgets.QGroupBox()
        group.setTitle(title)
        layout = QtWidgets.QHBoxLayout()

        @Slot(int)
        def title_callback(list_size):
            group.setTitle(f"{title} ({list_size})")

        list_view = QtWidgets.QListView()
        list_view.setModel(model)

        model.list_size_changed.connect(title_callback)

        layout.addWidget(list_view)
        group.setLayout(layout)

        return group



