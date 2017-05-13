from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from presentation.dialogs.AddAnotherObject import AddAnotherObject
from presentation.dialogs.TextDialog import TextDialog
from structure.enums.Items import Items
from structure.enums.NodeType import NodeType
from business.managers.PlayerTreeManager import PlayerTreeManager
from structure.enums.ObjectType import ObjectType
from structure.tree.Folder import Folder
from presentation.dialogs.NewTreeItem import NewTreeItem
from presentation.Translate import Translate as TR

from structure.tree.NodeObject import NodeObject
import sys
import traceback


class TreeWidget(QtWidgets.QFrame):
    """
    Tree widget for tree structure for templates (Spells, Items, Abilities, ...)
    data(0,11) -> Object in Node
    data(0,12) -> Node object
    """

    item_doubleclick_signal = QtCore.pyqtSignal(object)


    def __init__(self, parent, data_type: ObjectType = None, mainWindow=None):
        super().__init__(parent)

        self.tree_manager = PlayerTreeManager()

        self.mainWindow = mainWindow
        self.__data_type = data_type
        self.checking = False
        self.export_menu = ExportMenu(self)

        self.export_menu.export_button_signal.connect(self.export_data_slot)
        self.export_menu.export_html_signal.connect(self.export_html_slot)

        self.init_ui()
        self.draw_data()


    def keyPressEvent(self, key_event) -> None:
        """
        Map key shortcuts
        :param key_event: key event
        """
        if key_event.key() == QtCore.Qt.Key_Return:
            if self.treeWidget.selectedItems() and isinstance(self.treeWidget.selectedItems()[0].data(0, 12), NodeObject):
                self.item_doubleclick_signal.emit(self.treeWidget.selectedItems()[0])


    def init_ui(self):
        """
        Create basic UI frames and layouts
        """
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame")

        self.frame_layout = QtWidgets.QVBoxLayout(self)
        self.frame_layout.setObjectName("Frame layout")
        self.frame_layout.setContentsMargins(2, 2, 2, 0)
        self.frame_layout.setSpacing(1)

        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        font = QtGui.QFont()
        font.setPointSize(18)
        self.treeWidget.setFont(font)
        self.treeWidget.setHeaderLabel(TR().tr(self.__data_type))
        self.treeWidget.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.treeWidget.header().setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.treeWidget.header().setFrameShadow(QtWidgets.QFrame.Sunken)
        self.treeWidget.header().setLineWidth(2)

        # self.treeWidget.header().setFrameShadow(QtWidgets.QFrame.Plain)

        self.treeWidget.setDragDropMode(self.treeWidget.InternalMove)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setDropIndicatorShown(True)

        self.main_drop_event = self.treeWidget.dropEvent
        self.treeWidget.dropEvent = self.custom_drop_event

        self.frame_layout.addWidget(self.treeWidget)

        self.init_buttons()
        self.init_context_menu()


    def custom_drop_event(self, event: object) -> None:
        """
        Custom drop event, call base drop event and update structure of tre
        :param event: drop event
        """
        self.main_drop_event(event)
        count_root = self.treeWidget.topLevelItemCount()
        for i in range(count_root):
            self.update_structure(self.treeWidget.topLevelItem(i))
        self.draw_data()


    def update_structure(self, node: object, parent_id: int = None) -> None:
        """
        Update sructure of tree (recursion)
        :param node: Current node in tree
        :param parent_id: parent_id
        """
        updated = self.tree_manager.update_node_parent(node.data(0, 12), parent_id,
                                                       self.__data_type)
        # if not updated:
        child_count = node.childCount()
        for n in range(child_count):
            self.update_structure(node.child(n), node.data(0, 12).id)


    def init_context_menu(self) -> None:
        """
        Prepare tree items for contest menu
        """
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)
        self.treeWidget.itemDoubleClicked.connect(self.double_click_item_slot)


    def openMenu(self, position) -> None:
        """
        Create contest menu items
        :param position: selected item in tree
        """
        indexes = self.treeWidget.selectedIndexes()

        if indexes:
            item_type = indexes[0].data(12).nodeType
            item_id = indexes[0].data(12).id
            item = indexes[0].data(12)
            targetObject = indexes[0].data(11)

            menu = QtWidgets.QMenu()

            if isinstance(item, NodeObject) and item.object.object_type is ObjectType.ITEM and (
                            item.object.parent_id == -1 or item.object.parent_id == -2):
                pass
            else:
                delete_action = QtWidgets.QAction(TR().tr('Delete'), menu)
                delete_action.setData(QtCore.QVariant('delete'))
                menu.addAction(delete_action)

            rename_action = QtWidgets.QAction(TR().tr('Rename'), menu)
            rename_action.setData(QtCore.QVariant('rename'))
            menu.addAction(rename_action)

            if item_type == NodeType.FOLDER.value:
                folder_action = QtWidgets.QAction(TR().tr('New_item'), menu)
                folder_action.setData(QtCore.QVariant('new'))
                menu.addAction(folder_action)
                delete_action = QtWidgets.QAction(TR().tr('Import'), menu)
                delete_action.setData(QtCore.QVariant('import'))
                menu.addAction(delete_action)

            node = self.tree_manager.get_node(item_id)
            if self.tree_manager.have_tree_children(node):
                add_object_action = QtWidgets.QAction(TR().tr('Add_object'), menu)
                add_object_action.setData(QtCore.QVariant('add_object'))
                menu.addAction(add_object_action)

            action = menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
            if action:
                self.contest_menu_actions(action, item, targetObject)


    def contest_menu_actions(self, action, node, targetObject):
        """
            Do action based on contest menu selected
        :param action: selected action
        :param item_id: item id (ID in player tree structure)
        """
        # XXXXXXXXXXXXXXXXXX DELETE ACTION XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        if action.data() == 'delete':
            self.tree_manager.delete_node(node, targetObject)
            # self.mainWindow.redraw_context_widget(None, None)
            self.draw_data()
            self.mainWindow.tabWidget.clear_tab_widget()
        # XXXXXXXXXXXXXXXXXX NEW ITEM ACTION XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        elif action.data() == 'new':
            data, choice = NewTreeItem.get_data(
                self.__data_type.instance()().children + [self.__data_type.instance()])
            if choice:
                self.tree_manager.create_node(data['NodeType'], data['name'], node.id,
                                              self.__data_type, data['NodeObject'])
                self.draw_data()
        # XXXXXXXXXXXXXXXXXX IMPORT DATA ACTION XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        elif action.data() == 'import':
            self.import_data_slot(node.id)

        # XXXXXXXXXXXXXXXXX RENAME NODE ACTION XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        elif action.data() == 'rename':
            obj = node
            text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
                                                      TR().tr('New_name'), text=obj.name)
            if ok:
                obj.name = text
                self.tree_manager.update_node(obj)

            self.draw_data()

        # XXXXXXXXXXXXXXXX ADD OBJECT FROM OTHER ACTION XXXXXXXXXXXXXXXXXXXXXXXX
        elif action.data() == 'add_object':
            data, ok = AddAnotherObject.get_data(node)
            print(data)
            if ok:
                for type, items in data.items():

                    for item in items:
                        nodeObject = self.tree_manager.get_node(item)
                        newObject = nodeObject.object.DAO()().get(nodeObject.object.id, None, nodeObject.id,
                                                                  nodeObject.object.object_type)

                        newObject.DAO()().create(newObject, node.id, self.__data_type)

            self.draw_data()


    def init_buttons(self):
        """
        Create buttons under tree widget
        """
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(5)
        buttons_layout.setObjectName("Buttons layout")
        spacer = QtWidgets.QSpacerItem(40, 20,
                                       QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Minimum)
        buttons_layout.addItem(spacer)

        # Import button
        import_button = QtWidgets.QPushButton(self)
        import_button.setObjectName('TreeImportButton')
        import_icon = QtGui.QIcon()
        import_icon.addPixmap(QtGui.QPixmap("resources/icons/import.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)
        import_button.setIcon(import_icon)
        import_button.clicked.connect(lambda: self.import_data_slot())
        import_button.setStatusTip(TR().tr('tip.Import_templates'))

        buttons_layout.addWidget(import_button)

        # Export button
        export_button = QtWidgets.QPushButton(self)
        export_button.setObjectName('TreeExportButton')
        export_icon = QtGui.QIcon()
        export_icon.addPixmap(QtGui.QPixmap("resources/icons/export.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)
        export_button.setIcon(export_icon)
        export_button.clicked.connect(self.export_menu.create_menu)
        export_button.setStatusTip(TR().tr('tip.Export_templates'))

        buttons_layout.addWidget(export_button)

        # New button
        new_button = QtWidgets.QPushButton(self)
        new_button.setObjectName('TreeNewButton')
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap("resources/icons/plus.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        new_button.setIcon(new_icon)
        new_button.clicked.connect(self.__button_new_action)
        new_button.setStatusTip(TR().tr('tip.New_root_node'))

        buttons_layout.addWidget(new_button)

        self.frame_layout.addLayout(buttons_layout)


    def __button_new_action(self):
        """
        Clicked action on new button
        """
        data, choice = NewTreeItem.get_data(
            self.__data_type.instance()().children + [self.__data_type.instance()])
        if choice:
            if data['NodeType'] is NodeType.FOLDER:
                self.tree_manager.create_folder(data['name'], self.__data_type)
            else:
                newObject = data['NodeObject']()
                newObject.name = data['name']

                newObject.DAO()().create(newObject, None, self.__data_type)

            self.draw_data()


    def draw_data(self):
        """
        Redraw items in tree widget, same expanded/collapsed items
        """

        expanded_indexes = {}

        it = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        while it.value():
            node_id = it.value().data(0, 12).id
            expanded_indexes.update({node_id: it.value().isExpanded()})
            it += 1

        self.treeWidget.clear()

        items = self.tree_manager.get_tree(self.__data_type)

        self.set_items(items)

        it = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        while it.value():
            if it.value().data(0, 12).id in expanded_indexes and \
                    expanded_indexes[it.value().data(0, 12).id]:
                it.value().setExpanded(True)
            it += 1


    def set_items(self, items: list, parent=None, recursion=1):
        """
        Create item tree in widget
        :param items: object items
        :param parent: id of parent item (recursion)
        """
        if parent is None:
            parent = self.treeWidget

        for item in items:
            tree_item = QtWidgets.QTreeWidgetItem(parent)
            tree_item.setText(0, item.name)

            tree_item.setData(0, 12, QtCore.QVariant(item))

            if isinstance(item, Folder):
                folder_icon = QtGui.QIcon()
                folder_icon.addPixmap(QtGui.QPixmap("resources/icons/open.png"),
                                      QtGui.QIcon.Normal, QtGui.QIcon.Off)
                tree_item.setIcon(0, folder_icon)
                tree_item.setFlags(
                    tree_item.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.set_items(item.children, tree_item)

            else:

                icon = item.object.icon
                object_icon = QtGui.QIcon(icon)
                tree_item.setIcon(0, object_icon)
                tree_item.setFlags(
                    tree_item.flags() | QtCore.Qt.ItemIsUserCheckable)

                self.set_items(item.children, tree_item, recursion + 1)

                tree_item.setData(0, 11, QtCore.QVariant(item.object))

            if self.checking:
                if isinstance(item, NodeObject) and self.__data_type is item.object.object_type:
                    tree_item.setCheckState(0, QtCore.Qt.Unchecked)
                if self.tree_manager.tree_folder(item):
                    tree_item.setCheckState(0, QtCore.Qt.Unchecked)


    def export_data_slot(self):
        """
        Slot for export all selected objects in tree to file
        :return:
        """
        it = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        checked_items = []
        while it.value():
            if it.value().checkState(0) and it.value().data(0, 12).nodeType is NodeType.OBJECT:
                checked_items.append(it.value().data(0, 12).id)
            it += 1

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        types = "Xml Files (*.xml)"
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, TR().tr("File_select_target"),
                                                            "", types, options=options)
        if fileName:
            self.tree_manager.export_to_xml(checked_items, fileName)
            TextDialog('Export complete')


    def export_html_slot(self) -> None:
        """
        Slot for xport all selected objects to HTML files
        :return: 
        """
        it = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        checked_items = []
        while it.value():
            if it.value().checkState(0) and it.value().data(0, 12).nodeType is NodeType.OBJECT:
                checked_items.append(it.value().data(0, 12).id)
            it += 1

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        types = "Html Files (*.html)"
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, TR().tr("File_select_target"),
                                                            "", types, options=options)
        if fileName:
            self.tree_manager.export_to_html(checked_items, fileName)
            TextDialog('Export complete')


    def import_data_slot(self, parent=None):
        """
        Slot for import xml from file
        :param parent: parent node, import to witch folder
        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        types = "Xml Files (*.xml)"
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, TR().tr("File_select_open"),
                                                            "", types, options=options)
        if fileName:
            try:
                self.tree_manager.import_from_xml(fileName, self.__data_type, parent, True)
            except Exception as e:
                print(e)
                traceback.print_exc(file=sys.stderr)
                TextDialog('Export failed')
            self.draw_data()


    def double_click_item_slot(self, item):
        """
        Emit double click signal
        :param item: item clicked on
        """
        if item.data(0, 12).nodeType.value is not 1:
            # Skip inventory and ground
            obj = item.data(0, 12).object
            if not (obj.object_type is ObjectType.ITEM and obj.type is Items.CONTAINER and (
                            obj.parent_id == -1 or obj.parent_id == -2)):
                self.item_doubleclick_signal.emit(item)
        if item.isExpanded():
            item.setExpanded(False)
        else:
            item.setExpanded(True)


class ExportMenu(QtWidgets.QHBoxLayout):
    """
    Class for pop up menu in tree widget for xport
    """
    export_button_signal = QtCore.pyqtSignal()
    export_html_signal = QtCore.pyqtSignal()


    def __init__(self, parent):
        super().__init__()
        self.__parent = parent


    def create_menu(self):
        """
        Create pop up menu with buttons
        """
        if self.__parent.checking:
            return

        self.__parent.checking = True
        self.__parent.draw_data()
        self.export_menu_layout = QtWidgets.QHBoxLayout()
        self.export_menu_layout.setSpacing(5)
        self.export_menu_layout.setObjectName("Buttons layout")

        button_export = QtWidgets.QPushButton("Export XML")
        button_exportHTML = QtWidgets.QPushButton("Export HTML")
        button_cancel = QtWidgets.QPushButton("Cancel")
        self.export_menu_layout.addWidget(button_export)
        self.export_menu_layout.addWidget(button_exportHTML)
        button_export.clicked.connect(self.export_button_signal)
        button_exportHTML.clicked.connect(self.export_html_signal)
        button_cancel.clicked.connect(self.export_buttons_cancel_slot)
        self.export_menu_layout.addWidget(button_cancel)

        # button_exportHTML.setDisabled(True)

        self.__parent.frame_layout.insertLayout(1, self.export_menu_layout)


    def export_buttons_cancel_slot(self):
        """
        Action when clicked on cancel button
        """
        self.__parent.checking = False

        while self.export_menu_layout.count():
            item = self.export_menu_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.export_menu_layout.clearLayout(item.layout())

        self.__parent.frame_layout.removeItem(self.export_menu_layout)
        self.__parent.draw_data()
