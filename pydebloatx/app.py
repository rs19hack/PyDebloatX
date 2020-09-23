from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPoint
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from gui_about import Ui_AboutWindow
from gui_main import Ui_MainWindow
import webbrowser
import subprocess
import img_res  # skipcq: PYL-W0611
import sys


__version__ = "1.6.0"


class Logic():
    def __init__(self):
        about.label_version.setText(f"Version {__version__}")
        self.total_size = 0
        self.is_link_menu = False
        self.main_title = 'Select the default Windows 10 apps to uninstall:\n(Hover over app names to view description)'
        self.store_title = 'Click on an app name to view it in Microsoft Store.'
        self.refresh_title = 'Refreshing list of installed apps...'
        self.size_text = 'MB'
        self.quit_dialog = 'Quit PyDebloatX?'
        self.dialog_yes = 'Yes'
        self.dialog_no = 'No'
        self.dialog_ok = 'OK'
        self.uninstall_text = 'Uninstall'
        self.uninstalling_text = 'Uninstalling'
        self.app_singular = 'app'
        self.app_genitive_singular = 'apps'
        self.app_genitive_plural = 'apps'
        self.size_available_text = 'MB of of disk space will be available.'

        self.apps_dict = {
            ui.checkBox: {"name": "*Microsoft.3DBuilder*", "link": "/?PFN=Microsoft.3DBuilder_8wekyb3d8bbwe", "size": 35.02},
            ui.checkBox_2: {"name": "*Microsoft.Microsoft3DViewer*", "link": "/?PFN=Microsoft.Microsoft3DViewer_8wekyb3d8bbwe", "size": 121.46},
            ui.checkBox_3: {"name": "*Microsoft.WindowsAlarms*", "link": "/?PFN=Microsoft.WindowsAlarms_8wekyb3d8bbwe", "size": 11.87},
            ui.checkBox_4: {"name": "*Microsoft.WindowsCalculator*", "link": "/?PFN=Microsoft.WindowsCalculator_8wekyb3d8bbwe", "size": 14.27},
            ui.checkBox_5: {"name": "*microsoft.windowscommunicationsapps*", "link": "/?PFN=Microsoft.windowscommunicationsapps_8wekyb3d8bbwe", "size": 245.78},
            ui.checkBox_6: {"name": "*Microsoft.WindowsCamera*", "link": "/?PFN=Microsoft.WindowsCamera_8wekyb3d8bbwe", "size": 49.05},
            ui.checkBox_7: {"name": "*Microsoft.GetHelp*", "link": "/?PFN=Microsoft.Gethelp_8wekyb3d8bbwe", "size": 11.89},
            ui.checkBox_8: {"name": "*Microsoft.ZuneMusic*", "link": "/?PFN=Microsoft.ZuneMusic_8wekyb3d8bbwe", "size": 50.34},
            ui.checkBox_9: {"name": "*Microsoft.WindowsMaps*", "link": "/?PFN=Microsoft.WindowsMaps_8wekyb3d8bbwe", "size": 39.80},

            ui.checkBox_10: {"name": "*Microsoft.Messaging*", "link": "/?PFN=Microsoft.Messaging_8wekyb3d8bbwe", "size": 30.08},
            ui.checkBox_11: {"name": "*Microsoft.BingFinance*", "link": "?productId=9WZDNCRFHV4V", "size": 32.82},
            ui.checkBox_12: {"name": "*Microsoft.ZuneVideo*", "link": "/?PFN=Microsoft.ZuneVideo_8wekyb3d8bbwe", "size": 51.80},
            ui.checkBox_13: {"name": "*Microsoft.BingNews*", "link": "?productId=9WZDNCRFHVFW", "size": 35.29},
            ui.checkBox_14: {"name": "*Microsoft.MicrosoftOfficeHub*", "link": "/?PFN=Microsoft.MicrosoftOfficeHub_8wekyb3d8bbwe", "size": 30.21},
            ui.checkBox_15: {"name": "*Microsoft.Office.OneNote*", "link": "/?PFN=Microsoft.Office.OneNote_8wekyb3d8bbwe", "size": 156.01},
            ui.checkBox_16: {"name": "*Microsoft.MSPaint*", "link": "/?PFN=Microsoft.MSPaint_8wekyb3d8bbwe", "size": 65.79},
            ui.checkBox_17: {"name": "*Microsoft.People*", "link": "/?PFN=Microsoft.People_8wekyb3d8bbwe", "size": 31.97},
            ui.checkBox_18: {"name": "*Microsoft.Windows.Photos*", "link": "/?PFN=Microsoft.Windows.Photos_8wekyb3d8bbwe", "size": 346.04},

            ui.checkBox_19: {"name": "*Microsoft.SkypeApp*", "link": "/?PFN=Microsoft.SkypeApp_kzf8qxf38zg5c", "size": 237.25},
            ui.checkBox_20: {"name": "*Microsoft.MicrosoftSolitaireCollection*", "link": "/?PFN=Microsoft.MicrosoftSolitaireCollection_8wekyb3d8bbwe", "size": 134.37},
            ui.checkBox_21: {"name": "*Microsoft.BingSports*", "link": "?productId=9WZDNCRFHVH4", "size": 30.92},
            ui.checkBox_22: {"name": "*Microsoft.Getstarted*", "link": "/?PFN=Microsoft.Getstarted_8wekyb3d8bbwe", "size": 19.53},
            ui.checkBox_23: {"name": "*Microsoft.WindowsSoundRecorder*", "link": "/?PFN=Microsoft.WindowsSoundRecorder_8wekyb3d8bbwe", "size": 12.40},
            ui.checkBox_24: {"name": "*Microsoft.BingWeather*", "link": "/?PFN=Microsoft.BingWeather_8wekyb3d8bbwe", "size": 32.32},
            ui.checkBox_25: {"name": "*Microsoft.WindowsFeedbackHub*", "link": "/?PFN=Microsoft.WindowsFeedbackHub_8wekyb3d8bbwe", "size": 35.02},
            ui.checkBox_26: {"name": "*xbox* | Where-Object {$_.name -notmatch 'xboxgamecallableui'}", "link": "/?PFN=Microsoft.XboxApp_8wekyb3d8bbwe", "size": 55.91},
            ui.checkBox_27: {"name": "*Microsoft.YourPhone*", "link": "/?PFN=Microsoft.YourPhone_8wekyb3d8bbwe", "size": 280.27}
        }

        ui.progressbar.setValue(0)
        ui.progressbar.setMaximum(len(self.apps_dict))
        ui.button_uninstall.clicked.connect(self.uninstall)
        ui.button_select_all.clicked.connect(self.select_all)
        ui.button_deselect_all.clicked.connect(self.deselect_all)
        ui.refresh_btn.clicked.connect(self.app_refresh)
        ui.refresh_bind.activated.connect(self.app_refresh)
        ui.store_btn.clicked.connect(self.store_menu)
        ui.store_bind.activated.connect(self.store_menu)
        ui.homepage_btn.clicked.connect(self.app_homepage)
        ui.homepage_bind.activated.connect(self.app_homepage)
        ui.about_btn.clicked.connect(self.app_about)
        ui.about_bind.activated.connect(self.app_about)
        ui.quit_btn.clicked.connect(self.app_quit)
        ui.quit_bind.activated.connect(self.app_quit)
        about.button_quit_about.clicked.connect(about.close)
        for i in self.apps_dict:
            i.clicked.connect(self.enable_buttons)
            with open("style.css", 'r') as file:
                i.setStyleSheet(file.read())

        self.workerThread = QThread()
        self.thread_list = []
        for item, i in enumerate(self.apps_dict):
            self.thread_list.append(CheckApps(self.apps_dict, i))
            self.thread_list[item].moveToThread(self.workerThread)
            self.thread_list[item].app_signal.connect(self.enable_installed)
            self.thread_list[item].progress_signal.connect(self.update_progress)
        self.app_refresh()

    def store_menu(self):
        if self.is_link_menu:
            self.is_link_menu = False
            ui.label_info.setText(self.main_title)
            ui.store_btn.setIcon(QIcon(':/icon/store_icon.png'))
            for i in self.apps_dict:
                i.setEnabled(False)
                i.setChecked(False)
            for i in self.installed_apps:
                i.setEnabled(True)
            self.enable_buttons()
            ui.button_select_all.show()
            ui.button_deselect_all.show()
            ui.button_uninstall.show()
            ui.label_note.show()
            ui.label_space.show()
            ui.label_size.show()
        else:
            self.is_link_menu = True
            ui.label_info.setText(self.store_title)
            ui.store_btn.setIcon(QIcon(':/icon/back_icon.png'))
            for i in self.apps_dict:
                i.setEnabled(True)
                i.setChecked(True)
            ui.button_select_all.hide()
            ui.button_deselect_all.hide()
            ui.button_uninstall.hide()
            ui.label_note.hide()
            ui.label_space.hide()
            ui.label_size.hide()

    def app_refresh(self):
        if self.is_link_menu:
            self.store_menu()
        self.installed_apps = []
        self.progress = 0
        for i in self.apps_dict:
            i.setEnabled(False)
            i.setChecked(False)
        ui.label_refresh.show()
        ui.label_info.hide()
        ui.progressbar.show()
        ui.refresh_btn.setDisabled(True)
        ui.refresh_bind.setEnabled(False)
        ui.store_btn.setDisabled(True)
        ui.store_bind.setEnabled(False)
        ui.button_select_all.setDisabled(True)
        ui.button_deselect_all.setDisabled(True)
        ui.button_uninstall.setDisabled(True)
        ui.refresh_btn.setIcon(QIcon(':/icon/no_refresh_icon.png'))
        ui.button_select_all.setIcon(QIcon(':/icon/no_check_icon.png'))
        ui.button_uninstall.setIcon(QIcon(':/icon/no_trash_icon.png'))
        ui.button_deselect_all.setIcon(QIcon(':/icon/no_cancel_icon.png'))
        QApplication.setOverrideCursor(QCursor(Qt.BusyCursor))
        ui.label_refresh.setText(self.refresh_title)
        for new_thread in self.thread_list:
            new_thread.start()

    def thread_finished(self):
        ui.progressbar.hide()
        ui.label_refresh.hide()
        ui.label_info.show()
        ui.progressbar.setValue(0)
        QApplication.setOverrideCursor(QCursor())
        ui.label_info.setText(self.main_title)
        ui.refresh_btn.setDisabled(False)
        ui.refresh_bind.setEnabled(True)
        ui.store_btn.setDisabled(False)
        ui.store_bind.setEnabled(True)
        ui.refresh_btn.setIcon(QIcon(':/icon/refresh_icon.png'))
        self.enable_buttons()

    def enable_installed(self, i):
        i.setEnabled(True)
        self.installed_apps.append(i)
        self.enable_buttons()

    def update_progress(self):
        self.progress += 1
        ui.progressbar.setValue(self.progress)
        if self.progress >= len(self.apps_dict):
            self.thread_finished()

    def enable_buttons(self):
        if not self.is_link_menu:
            self.total_size = 0
            for i in self.installed_apps:
                if i.isChecked():
                    self.total_size += self.apps_dict[i]["size"]
                    ui.label_size.setText(f'{self.total_size:.2f} {self.size_text}')
            if any(i.isChecked() for i in self.installed_apps):
                ui.button_uninstall.setDisabled(False)
                ui.button_deselect_all.setDisabled(False)
                ui.button_uninstall.setIcon(QIcon(':/icon/trash_icon.png'))
                ui.button_deselect_all.setIcon(QIcon(':/icon/cancel_icon.png'))
            else:
                ui.button_uninstall.setDisabled(True)
                ui.button_deselect_all.setDisabled(True)
                ui.button_uninstall.setIcon(QIcon(':/icon/no_trash_icon.png'))
                ui.button_deselect_all.setIcon(QIcon(':/icon/no_cancel_icon.png'))
                ui.label_size.setText(f'{self.total_size} {self.size_text}')

            if all(i.isChecked() for i in self.installed_apps):
                ui.button_select_all.setDisabled(True)
                ui.button_select_all.setIcon(QIcon(':/icon/no_check_icon.png'))
            else:
                ui.button_select_all.setDisabled(False)
                ui.button_select_all.setIcon(QIcon(':/icon/check_icon.png'))
        else:
            for i in self.apps_dict:
                if not i.isChecked():
                    i.setChecked(True)
                    webbrowser.open_new(f'ms-windows-store://pdp{self.apps_dict[i]["link"]}')

    @staticmethod
    def app_homepage():
        webbrowser.open_new('https://github.com/Teraskull/PyDebloatX')

    @staticmethod
    def app_about():
        about.setWindowModality(Qt.ApplicationModal)
        about.move(ui.geometry().center() - about.rect().center())
        about.show()

    def app_quit(self):
        pixmap = QPixmap('icon.ico').scaledToWidth(35, Qt.SmoothTransformation)
        msg_quit = QMessageBox()
        msg_quit.move(ui.geometry().center() - QPoint(83, 54))
        msg_quit.setText(self.quit_dialog)
        msg_yes = msg_quit.addButton(QMessageBox.Yes)
        msg_no = msg_quit.addButton(QMessageBox.No)
        msg_yes.setText(self.dialog_yes)
        msg_no.setText(self.dialog_no)
        msg_yes.setProperty('class', 'button_yes')
        msg_no.setProperty('class', 'button_no')
        msg_quit.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        msg_quit.setWindowIcon(QIcon('icon.ico'))
        msg_quit.setWindowTitle("PyDebloatX")
        msg_quit.setIconPixmap(pixmap)
        with open("style.css", 'r') as file:
            msg_quit.setStyleSheet(file.read())
        msg_quit_result = msg_quit.exec_()
        if msg_quit_result == QMessageBox.Yes:
            app.quit()

    def select_all(self):
        for i in self.installed_apps:
            if not i.isChecked():
                i.setChecked(True)
        self.enable_buttons()

    def deselect_all(self):
        for i in self.installed_apps:
            if i.isChecked():
                i.setChecked(False)
        self.enable_buttons()

    def uninstall(self):
        j = 0
        for i in self.installed_apps:
            if i.isChecked():
                j += 1
        pixmap = QPixmap('icon.ico').scaledToWidth(35, Qt.SmoothTransformation)

        msg_confirm = QMessageBox()
        msg_confirm.move(ui.geometry().center() - QPoint(145, 62))
        msg_confirm.setText(f"{self.uninstall_text} {j} {self.app_genitive_plural if j > 1 else self.app_singular}?\n\n{self.total_size:.2f} {self.size_available_text}")
        msg_yes = msg_confirm.addButton(QMessageBox.Yes)
        msg_no = msg_confirm.addButton(QMessageBox.No)
        msg_yes.setText(self.dialog_yes)
        msg_no.setText(self.dialog_no)
        msg_yes.setProperty('class', 'button_yes')
        msg_no.setProperty('class', 'button_no')
        msg_confirm.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        msg_confirm.setWindowIcon(QIcon('icon.ico'))
        msg_confirm.setWindowTitle("PyDebloatX")
        msg_confirm.setIconPixmap(pixmap)
        with open("style.css", 'r') as file:
            msg_confirm.setStyleSheet(file.read())
        msg_confirm_result = msg_confirm.exec_()

        if msg_confirm_result == QMessageBox.Yes:
            for i in self.apps_dict:
                if i.isChecked():
                    subprocess.Popen(["powershell", f'(Get-AppxPackage {self.apps_dict[i]["name"]} | Remove-AppxPackage)'], shell=True)
                    i.setChecked(False)
                    i.setEnabled(False)
                    self.installed_apps.remove(i)
            self.deselect_all()

            msg_proceed = QMessageBox()
            msg_proceed.move(ui.geometry().center() - QPoint(87, 54))
            msg_proceed.setText(f"{self.uninstalling_text} {j} {self.app_genitive_plural if j > 1 else self.app_singular}.")
            msg_ok = msg_proceed.addButton(QMessageBox.Ok)
            msg_ok.setText(self.dialog_ok)
            msg_ok.setProperty('class', 'button_yes')
            msg_proceed.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
            msg_proceed.setWindowTitle("PyDebloatX")
            msg_proceed.setIconPixmap(pixmap)
            with open("style.css", 'r') as file:
                msg_proceed.setStyleSheet(file.read())
            msg_proceed.exec_()


class CheckApps(QThread):
    progress_signal = pyqtSignal()
    app_signal = pyqtSignal(object)

    def __init__(self, apps_dict, i):
        super().__init__()
        self.apps_dict = apps_dict
        self.i = i

    def run(self):
        x = subprocess.Popen(["powershell", f'(Get-AppxPackage {self.apps_dict[self.i]["name"]}) -and $?'], stdout=subprocess.PIPE, shell=True)
        if x.communicate()[0].decode().strip() == "True":
            self.app_signal.emit(self.i)
        self.progress_signal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    about = Ui_AboutWindow()
    about.setupUi()
    ui = Ui_MainWindow()
    ui.setupUi()
    ui.show()
    logic = Logic()
    sys.exit(app.exec_())
