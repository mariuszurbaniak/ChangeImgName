from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel, QLineEdit
import os, exif

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWidget")
        browse_button = QPushButton("Browse")
        rename_button = QPushButton("Rename")
        browse_button.clicked.connect(self.button1_clicked)
        rename_button.clicked.connect(self.rename_images)
        
        
        prefix = QLabel("Prefix for filename: ")
        self.path_selected = QLabel()
        self.prefix = QLineEdit()
        self.instruction_text = QLabel('Browse to the folder containing images')
        self.path_selected_text = QLabel("Selected path: ")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(browse_button)
        button_layout.addWidget(rename_button)
        
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(prefix)
        prefix_layout.addWidget(self.prefix)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_selected_text)
        path_layout.addWidget(self.path_selected)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(prefix_layout)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(button_layout)
        
        
        self.setLayout(main_layout)
        
        
    def button1_clicked(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        self.path_selected_text.setText(self.folder_path)
        
        
    def rename_images(self):
        with os.scandir(self.folder_path) as directory:
            for image in directory:
                img = exif.Image(image)

                # check if file is valid image with exif data
                if img.has_exif:
                    # get image date from exif data
                    date = "".join("-".join(str(img.get("datetime_original")).split()).split(":"))
                    
                    # check for file duplicates
                    try:
                        os.rename(image, os.path.join(self.folder_path, f'{self.prefix.text()} {date}.jpg'))
                    except:
                        os.remove(image)
                else:
                    next()