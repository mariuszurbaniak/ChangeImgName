from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel, QLineEdit, QMainWindow, QProgressBar
import os, exif

class MainWindow(QMainWindow):
    num_of_images = 0
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rename Images")
        
        browse_button = QPushButton("Browse")
        rename_button = QPushButton("Rename")
        browse_button.clicked.connect(self.button1_clicked)
        rename_button.clicked.connect(self.rename_images)
        
        prefix_label = QLabel("Prefix for filename: ")
        path_selected = QLabel()
        self.prefix = QLineEdit()
        instruction_text = QLabel('Browse to the folder containing images')
        self.path_selected_text = QLabel("Selected path: ")
        
        main_widget = QWidget()
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(browse_button)
        button_layout.addWidget(rename_button)
        
        instruction_layout = QVBoxLayout()
        instruction_layout.addWidget(instruction_text)
        
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(prefix_label)
        prefix_layout.addWidget(self.prefix)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_selected_text)
        path_layout.addWidget(path_selected)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(instruction_layout)
        main_layout.addLayout(prefix_layout)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(button_layout)
        
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        
        self.statusbar = self.statusBar()     
        self.progressbar = QProgressBar()
        self.statusbar.addPermanentWidget(self.progressbar)       
 
        
        
        
        self.progressbar.setValue(MainWindow.num_of_images)
        
            
    
    def button1_clicked(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        self.path_selected_text.setText(self.folder_path)
        self.progressbar.setMaximum(len(list(os.scandir(self.folder_path))))
        
    
    
    def rename_images(self):
        with os.scandir(self.folder_path) as directory:
            for image in directory:
                MainWindow.num_of_images += 1
                self.progressbar.setValue(MainWindow.num_of_images)
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
                