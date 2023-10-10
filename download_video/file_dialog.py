import sys

from PySide2.QtWidgets import QApplication, QFileDialog, QWidget

class FileDialog():
    def download_path(self, project):
        app = QApplication([])  # Qt 어플리케이션 생성

        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly

        download_path = QFileDialog.getExistingDirectory(None, "Open Directory", "/westworld/show/%s" % project, options=options)

        if download_path:
            print(f"Selected directory: {download_path}")

        app.exec_
        return download_path
    
if __name__ == "__main__":
    fd = FileDialog()
    download_path = fd.download_path()
    print(download_path)
