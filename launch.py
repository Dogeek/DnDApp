from PyQt4 import QtCore, QtGui
import sys
from random import choice, randint

from lib import resources_rc
from lib.main_window_ui import Ui_MainWindow
from lib.host_window_ui import Ui_host_window
from lib.connect_window_ui import Ui_connect_window

from lib.functions import *

log("",True)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class main_window(Ui_MainWindow):
    '''
    This class inherits the Ui_Mainwindow class. The inheritance is 
    used to add bindings to launch the host/connect window dialog
    '''
    def __init__(self, MainWindow):
        self.main_window = MainWindow
        self.setupUi(self.main_window)
        self.ui_connect = Ui_connect_window()
        self.main_window.resize(1280,720)
        
        self.dock_campain.hide()
        self.dock_client.hide()
        
        self.actionHost_Game.triggered.connect(self.launch_host_game)
        self.actionConnect_to.triggered.connect(self.launch_connect_window)
        self.button_rollatable.clicked.connect(self.set_encounter_table)
        self.line_treasure_value.returnPressed.connect(self.set_treasure)

        self.list_of_encounters = ["_"]*12
        self.treasure_value = self.line_treasure_value.text()
        
        

    def launch_host_game(self):
        '''
        This method will launch the host window as a dialog.
        '''       
        host_dialog = QtGui.QDialog()
        ui = Ui_host_window()
        ui.setupUi(host_dialog)
        host_dialog.exec_()

    def launch_connect_window(self):
        '''
        This method will launch the connect window dialog
        '''
        connect_dialog = QtGui.QDialog()
        self.ui_connect.setupUi(connect_dialog)
        self.ui_connect.button_connect.clicked.connect(self.launch_dock_client)
        connect_dialog.exec_()
        if self.ui_connect.button_connect.isDown():
            connect_dialog.close()

    def launch_dock_client(self):
        self.dock_client.show()
        host_ip = self.ui_connect.line_host_ip.text()
        port = self.ui_connect.line_port.text()
        name = self.ui_connect.line_name.text()

    def set_encounter_table(self):
        environment=str(self.combo_environmentofencounter.currentText())
        del list_of_encounters
        list_of_encounters=get_random_encounters_table(get_monster_dict(),environment)
        self.label_nameofrolledmonster_1.setText(list_of_encounters[0])
        self.label_nameofrolledmonster_2.setText(list_of_encounters[1])
        self.label_nameofrolledmonster_3.setText(list_of_encounters[2])
        self.label_nameofrolledmonster_4.setText(list_of_encounters[3])
        self.label_nameofrolledmonster_5.setText(list_of_encounters[4])
        self.label_nameofrolledmonster_6.setText(list_of_encounters[5])
        self.label_nameofrolledmonster_7.setText(list_of_encounters[6])
        self.label_nameofrolledmonster_8.setText(list_of_encounters[7])
        self.label_nameofrolledmonster_9.setText(list_of_encounters[8])
        self.label_nameofrolledmonster_10.setText(list_of_encounters[9])
        self.label_nameofrolledmonster_11.setText(list_of_encounters[10])
        self.label_nameofrolledmonster_12.setText(list_of_encounters[11])

    def set_monster_stats(self):
        chance_of_encounter = self.slider_chanceofencounter.value()
        chosen_monster = get_a_monster(self.list_of_encounters, chance_of_encounter)
        life, ac, movement, attacks, damages, number_met, save_poison, save_wands,\
        save_paralysis, save_dragon, save_spells, moral, treasure, alignment,\
        xp_value = get_a_monster_stats(get_monster_dict(), chosen_monster)
        
        self.group_statsofrolledmonster.setTitle("Stats of Rolled Monster : {0}".format(chosen_monster))
        #self.label_statsofrolledmonster_ac

    def set_treasure(self):
        print("treasure_set!")
        try:
            treasure_value = int(self.treasure_value)
        except ValueError:
            self.line_treasure_value.setText("")
            pass
        has_gems = self.check_gems.isChecked()
        has_jewels = self.check_jewels.isChecked()
        has_magic = self.check_magic_items.isChecked()
        treasure = get_treasure(treasure_value, has_magic, has_gems, has_jewels)
        
        gem_string = ""
        jewel_string = ""
        magic_string = ""
        
        for gem_tuple in treasure["gems"]:
            gem_string += "{0} : {1}\n".format(gem_tuple[0], gem_tuple[1])
        for jewel_tuple in treasure["jewels"]:
            jewel_string += "{0} : {1}\n".format(jewel_tuple[0], jewel_tuple[1])
        for magic_item in treasure["magic_items"]:
            magic_string += magic_item
        self.display_gems.setPlainText(gem_string)
        self.display_jewels.setPlainText(jewel_string)
        self.display_magicitems.setPlainText(magic_string)
        self.lineedit_numberofcoins_platinum.setText(treasure["pieces"][0])
        self.lineedit_numberofcoins_gold.setText(treasure["pieces"][1])
        self.lineedit_numberofcoins_electrum.setText(treasure["pieces"][2])
        self.lineedit_numberofcoins_silver.setText(treasure["pieces"][3])
        self.lineedit_numberofcoins_copper.setText(treasure["pieces"][4])
        self.main_window.update()

app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = main_window(MainWindow)
MainWindow.show()
sys.exit(app.exec_())