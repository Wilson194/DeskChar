from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

from structure.enums.NodeType import NodeType
from managers.PlayerTreeManager import PlayerTreeManager
from structure.enums.ObjectType import ObjectType
from structure.tree.Folder import Folder
from presentation.dialogs.NewTreeItem import NewTreeItem
from presentation.Translate import Translate as TR


class TreeWidget(QtWidgets.QFrame):
    """
    Tree widget for tree structure for templates (Spells, Items, Abilities, ...)
    data(0,5) -> ID
    data(0,6) -> Type
    """

    item_doubleclick_signal = QtCore.pyqtSignal(object)

    def __init__(self, parent, data_type: ObjectType = None):
        super().__init__(parent)

        self.tree_manager = PlayerTreeManager()

        self.__data_type = data_type

        self.init_ui()
        self.draw_data()


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
        font.setPointSize(13)
        self.treeWidget.setFont(font)
        self.treeWidget.setHeaderLabel(TR().tr(self.__data_type))
        self.treeWidget.header().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.treeWidget.setDragDropMode(self.treeWidget.InternalMove)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setDropIndicatorShown(True)

        self.main_drop_event = self.treeWidget.dropEvent
        self.treeWidget.dropEvent = self.custom_drop_event

        self.frame_layout.addWidget(self.treeWidget)

        self.init_buttons()
        self.init_context_menu()


    def custom_drop_event(self, event):
        """
        Custom drop event, call base drop event and update structure of tre
        :param event: drop event
        """
        self.main_drop_event(event)

        count_root = self.treeWidget.topLevelItemCount()
        for i in range(count_root):
            self.update_structure(self.treeWidget.topLevelItem(i))

        self.draw_data()


    def update_structure(self, node, parent_id=None):
        """
        Update sructure of tree (recursion)
        :param node: Current node in tree
        :param parent: parent_id
        """
        self.tree_manager.update_node_parent(node.data(0, 5), parent_id)
        child_count = node.childCount()
        for n in range(child_count):
            self.update_structure(node.child(n), node.data(0, 5))


    def init_context_menu(self):
        """
        Prepare tree items for contest menu
        """
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)
        self.treeWidget.itemDoubleClicked.connect(self.double_click_item)


    def openMenu(self, position):
        """
        Create contest menu items
        :param position: selected item in tree
        """
        indexes = self.treeWidget.selectedIndexes()

        item_type = indexes[0].data(6)
        item_id = indexes[0].data(5)
        if item_type == NodeType.FOLDER.value:
            menu = QtWidgets.QMenu()
            delete_action = QtWidgets.QAction(TR().tr('Delete'), menu)
            delete_action.setData(QtCore.QVariant('delete'))
            menu.addAction(delete_action)
            folder_action = QtWidgets.QAction(TR().tr('New_item'), menu)
            folder_action.setData(QtCore.QVariant('new'))
            menu.addAction(folder_action)
            action = menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
            if action:
                self.contest_nemu_actions(action, item_id)


    def contest_nemu_actions(self, action, item_id):
        """
            Do action based on contest menu selected
        :param action: selected action
        :param item_id: item id (ID in player tree structure)
        """
        if action.data() == 'delete':
            self.tree_manager.delete_node(item_id)
            self.draw_data()
        elif action.data() == 'new':
            data, choice = NewTreeItem.get_data()
            if choice:
                self.tree_manager.create_node(NodeType(int(data['type'])), data['name'], item_id,
                                              self.__data_type)
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

        new_button = QtWidgets.QPushButton(self)
        new_button.setObjectName('TreeNewButton')
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap("resources/icons/plus.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        new_button.setIcon(new_icon)
        new_button.clicked.connect(self.__button_new)
        new_button.setStatusTip(TR().tr('tip.New_root_node'))

        buttons_layout.addWidget(new_button)

        delete_button = QtWidgets.QPushButton(self)
        delete_button.setObjectName('TreeNewButton')
        delete_icon = QtGui.QIcon()
        delete_icon.addPixmap(QtGui.QPixmap("resources/icons/minus.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)
        delete_button.setIcon(delete_icon)

        buttons_layout.addWidget(delete_button)

        self.frame_layout.addLayout(buttons_layout)


    def __button_new(self):
        """
        Clicked action on new button
        """
        data, choice = NewTreeItem.get_data()
        if choice:
            self.tree_manager.create_node(NodeType(int(data['type'])), data['name'], None,
                                          self.__data_type)
            self.draw_data()


    def draw_data(self):
        """
        Redraw items in tree widget, same expanded/collapsed items
        """

        expanded_indexes = {}
        it = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        while it.value():
            node_id = it.value().data(0, 5)
            expanded_indexes.update({node_id: it.value().isExpanded()})
            it += 1

        self.treeWidget.clear()
        if self.__data_type is ObjectType.SPELL:
            items = self.tree_manager.get_spell_tree()
        else:
            items = []

        self.set_items(items)

        it = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        while it.value():
            if it.value().data(0, 5) in expanded_indexes and \
                    expanded_indexes[it.value().data(0, 5)]:
                it.value().setExpanded(True)
            it += 1


    def set_items(self, items: list, parent=None):
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
            tree_item.setData(0, 5, QtCore.QVariant(item.id))

            if isinstance(item, Folder):
                folder_icon = QtGui.QIcon()
                folder_icon.addPixmap(QtGui.QPixmap("resources/icons/open.png"),
                                      QtGui.QIcon.Normal, QtGui.QIcon.Off)
                tree_item.setIcon(0, folder_icon)
                self.set_items(item.children, tree_item)
                tree_item.setData(0, 6, QtCore.QVariant(NodeType.FOLDER.value))
            else:
                object_icon = QtGui.QIcon()
                object_icon.addPixmap(QtGui.QPixmap("resources/icons/book.png"),
                                      QtGui.QIcon.Normal, QtGui.QIcon.Off)
                tree_item.setIcon(0, object_icon)
                tree_item.setData(0, 6, QtCore.QVariant(NodeType.OBJECT.value))


    def double_click_item(self, item):
        self.item_doubleclick_signal.emit(item)
