from PyQt5 import QtWidgets, QtGui, QtCore
import numpy
import math

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap, QIcon
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, \
    QGraphicsItem, QAction, QGraphicsPixmapItem
from PyQt5.QtWidgets import QToolBar

from business.managers.MapManager import MapManager
from data.DAO.MapDAO import MapDAO
from data.DAO.MapItemDAO import MapItemDAO
from presentation.dialogs.EditMapItem import EditMapItem
from presentation.dialogs.NewMapItem import NewMapItem
from structure.enums.MapItem import MapItemType
from structure.enums.ObjectType import ObjectType
from structure.map.Map import Map
from structure.map.MapItem import MapItem
from presentation.Translate import Translate as TR


class MapWidget(QtWidgets.QFrame):
    """
    Custom tab widget with function for editing templates
    """

    mapItem_delete_signal = QtCore.pyqtSignal(object)


    def __init__(self, parent, mainWindow):
        super().__init__(parent)

        self.mainWindow = mainWindow
        self.mapManager = MapManager()

        self.map = None

        self.init_bar()
        self.init_ui()

        self.mapItem_delete_signal.connect(self.item_delete_slot)


    def init_ui(self):
        """
        Init map widget UI
        :return: 
        """
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.frameLayout = QtWidgets.QVBoxLayout(self)
        self.frameLayout.setObjectName("Frame layout")

        self.grview = QGraphicsView()
        self.grview.setRenderHints(self.grview.renderHints() | QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.scene = QGraphicsScene()

        # scene.setSceneRect(0, 0, 1500, 459)

        self.grview.setScene(self.scene)

        noMap = QPixmap('resources/icons/no_map.png')
        self.scene.addPixmap(noMap)
        self.grview.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        self.frameLayout.addWidget(self.grview)


    def init_bar(self):
        """
        Init function bar
        :return: 
        """
        toolbar = QToolBar()
        toolbar.setObjectName('MapToolbar')
        self.mainWindow.addToolBar(Qt.RightToolBarArea, toolbar)

        # ------------------------------- Open map ----------------------------------
        self.openMap_action = QAction(QIcon('resources/icons/openMap.png'), TR().tr('Open_map'), self.mainWindow,
                                      triggered=self.open_map_action, enabled=False)
        toolbar.addAction(self.openMap_action)

        # ------------------------------- Zoom in ----------------------------------
        self.zoomIn_action = QAction(QIcon('resources/icons/zoomIn.png'), TR().tr('Zoom_in'), self.mainWindow,
                                     triggered=self.zoom_in_action, shortcut='Ctrl++', enabled=False)
        toolbar.addAction(self.zoomIn_action)

        # ------------------------------- Zoom out ----------------------------------
        self.zoomOut_action = QAction(QIcon('resources/icons/zoomOut.png'), TR().tr('Zoom_out'), self.mainWindow,
                                      triggered=self.zoom_out_action, shortcut='Ctrl++', enabled=False)
        toolbar.addAction(self.zoomOut_action)

        # ------------------------------- Edit info  ----------------------------------
        self.info_action = QAction(QIcon('resources/icons/heart.png'), TR().tr('Edit_info'), self.mainWindow,
                                   triggered=self.edit_info_action, shortcut='Ctrl+P', enabled=False)
        toolbar.addAction(self.info_action)

        toolbar.addSeparator()

        # ------------------------------- Add monster ----------------------------------
        self.addMonster_action = QAction(QIcon('resources/icons/addMonster.png'), TR().tr('Add_monster'), self.mainWindow,
                                         triggered=self.add_monster_action, shortcut='Ctrl+M', enabled=False)
        toolbar.addAction(self.addMonster_action)

        # ------------------------------- Add item ----------------------------------
        self.addItem_action = QAction(QIcon('resources/icons/addItem.png'), TR().tr('Add_item'), self.mainWindow,
                                      triggered=self.add_item_action, enabled=False)
        toolbar.addAction(self.addItem_action)

        # ------------------------------- Add room ----------------------------------
        self.addRoom_action = QAction(QIcon('resources/icons/addRoom.png'), TR().tr('Add_room'), self.mainWindow,
                                      triggered=self.add_room_action, enabled=False)
        toolbar.addAction(self.addRoom_action)

        # ------------------------------- Add object ----------------------------------
        self.addObject_action = QAction(QIcon('resources/icons/addObject.png'), TR().tr('Add_object_map'), self.mainWindow,
                                        triggered=self.add_object_action, enabled=False)
        toolbar.addAction(self.addObject_action)


    def enable_tool_bar(self):
        """
        Enable tool bar actions
        """
        self.openMap_action.setEnabled(True)
        self.zoomIn_action.setEnabled(True)
        self.zoomOut_action.setEnabled(True)
        self.info_action.setEnabled(True)

        self.addItem_action.setEnabled(True)
        self.addRoom_action.setEnabled(True)
        self.addMonster_action.setEnabled(True)
        self.addObject_action.setEnabled(True)


    def tree_item_doubleclick_action(self, item):
        """
        Slot for double click on map at tree widget
        :param item: item in tree widget
        """

        if self.map:
            self.save_map()

        if item.data(0, 11).object_type is not ObjectType.MAP:
            self.mainWindow.redraw_context_widget(item.data(0, 11).object_type, item)
        else:

            self.enable_tool_bar()
            map = MapDAO().get(item.data(0, 11).id)

            if self.map and self.map.id == map.id:
                map = MapDAO().get(item.data(0, 11).id)
            self.map = map
            self.redraw()


    def item_delete_slot(self, mapItem):
        # mapItem.number
        self.map.mapItemDraws.remove(self.map.mapItemDraws[mapItem.number - 1])
        MapItemDAO().delete(mapItem.mapItem.id)
        # self.redraw()


    def save_map(self):
        """
        Save image of map
        :return:
        """
        self.mapManager.update(self.map)
        self.save_map_action()


    def redraw(self):
        """
        Redraw scene in widget
        """
        self.scene.clear()
        if self.map.mapFile:
            pixMap = QPixmap(self.map.mapFile)
            sceneMap = self.scene.addPixmap(pixMap)
            self.map.mapPixMap = sceneMap
            self.grview.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

        for num, mapItem in enumerate(self.map.mapItems):
            mapItem.number = num + 1
            item = MapItemDraw(mapItem, self.mapItem_delete_signal)
            self.scene.addItem(item)
            self.map.addMapItemDraws(item)


    def open_map_action(self):
        """
        Open image with map slot
        """
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, "Open File",
                                                            QtCore.QDir.currentPath())

        if fileName:
            if self.map.mapPixMap:
                self.scene.removeItem(self.map.mapPixMap)

            fileName = self.mapManager.copy_map(fileName, self.map)
            self.map.mapFile = fileName
            self.map.mapPixMap = self.scene.addPixmap(QPixmap(fileName))
            self.grview.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)


    def zoom_in_action(self):
        """
        Zoom in whole map widget
        """
        self.grview.scale(1.2, 1.2)


    def zoom_out_action(self):
        """
        Zoom out whole map widget
        """
        self.grview.scale(0.8, 0.8)


    def add_item_action(self):
        """
        Add item to map
        :return:
        """
        data, choice = NewMapItem.get_data()

        if choice:
            number = len(self.map.mapItemDraws) + 1
            mapItem = MapItem(None, data.get('name', ''), data.get('description', ''), QPointF(), 0, number, None, self.map.id,
                              MapItemType.ITEM)
            id = MapItemDAO().create(mapItem)
            mapItem.id = id
            item = MapItemDraw(mapItem, self.mapItem_delete_signal)
            self.scene.addItem(item)

            self.map.addMapItemDraws(item)


    def add_monster_action(self):
        """
        Add monster to map
        :return:
        """
        data, choice = NewMapItem.get_data()

        if choice:
            number = len(self.map.mapItemDraws) + 1
            mapItem = MapItem(None, data.get('name', ''), data.get('description', ''), QPointF(), 0, number, None, self.map.id,
                              MapItemType.MONSTER)
            id = MapItemDAO().create(mapItem)
            mapItem.id = id
            item = MapItemDraw(mapItem, self.mapItem_delete_signal)
            self.scene.addItem(item)

            self.map.addMapItemDraws(item)


    def add_room_action(self):
        """
        Add room to map
        :return:
        """
        data, choice = NewMapItem.get_data()

        if choice:
            number = len(self.map.mapItemDraws) + 1
            mapItem = MapItem(None, data.get('name', ''), data.get('description', ''), QPointF(), 0, number, None, self.map.id,
                              MapItemType.ROOM)
            id = MapItemDAO().create(mapItem)
            mapItem.id = id
            item = MapItemDraw(mapItem, self.mapItem_delete_signal)
            self.scene.addItem(item)

            self.map.addMapItemDraws(item)


    def add_object_action(self):
        """
        Add object to map
        :return:
        """
        data, choice = NewMapItem.get_data()

        if choice:
            number = len(self.map.mapItemDraws) + 1
            mapItem = MapItem(None, data.get('name', ''), data.get('description', ''), QPointF(), 0, number, None, self.map.id,
                              MapItemType.OBJECT)
            id = MapItemDAO().create(mapItem)
            mapItem.id = id
            item = MapItemDraw(mapItem, self.mapItem_delete_signal)
            self.scene.addItem(item)

            self.map.addMapItemDraws(item)

    def edit_info_action(self):
        data, choice = EditMapItem.get_data(None, self.map)
        if choice:
            self.map.name = data['name']
            self.map.description = data['description']

    def save_map_action(self):
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

        img = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        img.fill(Qt.transparent)

        painter = QPainter(img)
        self.scene.render(painter)

        name = 'resources/maps/exportedMap-{}.png'.format(self.map.id)
        img.save(name)

        del painter


    def drawItems(self, painter, items, options, widget=None):
        pass


class MapItemDraw(QGraphicsPixmapItem):
    """
    Class for handling icon on scene
    """
    HANDLE_SIZE = 8


    def __init__(self, mapItem: MapItem, signal):
        # Create backup of pixmap
        pix = QPixmap(mapItem.itemType.icon())
        self.oldPic = pix
        super().__init__(pix)

        self.mapItem = mapItem
        self.signal = signal

        # Set ignore transparent background for mouse
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

        # Set position in front of background
        self.setZValue(50)
        self.topLeftHandle = None
        self.botRightHandle = None

        # Set position of image
        self.setPos(mapItem.coord)

        # Rescale image to correct size
        scaleX = pix.width() + mapItem.scale
        scaleY = pix.height() + mapItem.scale
        npix = pix.scaled(scaleX, scaleY, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(npix)

        # Set resize coefficient
        self.resize = mapItem.scale
        self.actualResize = None

        # Set number and object
        self.number = mapItem.number
        self.targetObject = None

        self.selectedHandle = None
        self.mousePressPos = None
        self.mousePressRect = None

        self.setAcceptHoverEvents(True)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.mapItem.name = self.mapItem.name if self.mapItem.name else ''
        self.mapItem.description = self.mapItem.description if self.mapItem.description else ''
        toolTip = self.mapItem.name + '\n\n  ' + self.mapItem.description
        self.setToolTip(toolTip)


    def get_object(self) -> MapItem:
        """
        Return object MapItem for saving to database
        :return: MapItem
        """
        self.mapItem.coord = self.pos()
        self.mapItem.scale = self.resize

        return self.mapItem


    def paint(self, painter, option, widget=None):
        """
        Overwrite function for draw pixmap, add number and resize
        :param painter: 
        :param option: 
        :param widget: 
        :return: 
        """
        super().paint(painter, option, widget)

        # Paint number
        font = painter.font()
        font.setPointSize(self.pixmap().height() / 6)
        painter.setFont(font)
        painter.drawText(self.boundingRect(), str(self.number))

        # Paint resize
        if self.isSelected():
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
            painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            s = self.HANDLE_SIZE + self.resize / 100
            leftHandleRect = QRectF(self.boundingRect().left(), self.boundingRect().top(), s, s)
            painter.drawEllipse(leftHandleRect)
            self.topLeftHandle = leftHandleRect

            rightHandleRect = QRectF(self.boundingRect().right() - s,
                                     self.boundingRect().bottom() - s,
                                     s, s)
            painter.drawEllipse(rightHandleRect)
            self.botRightHandle = rightHandleRect


    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            if self.topLeftHandle.contains(moveEvent.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.botRightHandle.contains(moveEvent.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        super().hoverMoveEvent(moveEvent)


    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """

        if self.isSelected():
            if self.topLeftHandle.contains(mouseEvent.pos()):
                self.selectedHandle = self.topLeftHandle
            if self.botRightHandle.contains(mouseEvent.pos()):
                self.selectedHandle = self.botRightHandle

            if self.selectedHandle:
                self.mousePressPos = mouseEvent.pos()
                self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)


    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.selectedHandle = None
        self.mousePressPos = None
        self.mousePressRect = None

        if self.actualResize:
            self.resize = self.actualResize
        self.update()


    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.selectedHandle is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)


    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)


    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        x1 = self.mousePressPos.x()
        x2 = self.mousePressPos.y()

        y1 = mousePos.x()
        y2 = mousePos.y()

        if self.selectedHandle == self.topLeftHandle:
            resize = min((x1 - y1), (x2 - y2))
            scaleX = self.oldPic.width() + resize + self.resize
            scaleY = self.oldPic.height() + resize + self.resize
        else:
            resize = min((y1 - x1), (y2 - x2))
            scaleX = self.oldPic.width() + resize + self.resize
            scaleY = self.oldPic.height() + resize + self.resize

        self.actualResize = resize + self.resize

        npix = self.oldPic.scaled(scaleX, scaleY, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.setPixmap(npix)


    def mouseDoubleClickEvent(self, mouseEvent):
        data, choice = EditMapItem.get_data(None, self.mapItem)
        if choice:
            self.mapItem.name = data.get('name')
            self.mapItem.description = data.get('description')


    def keyReleaseEvent(self, keyEvent):
        if keyEvent.key() == QtCore.Qt.Key_Delete:
            quit_msg = "Are you sure you want to delete this?"
            reply = QtWidgets.QMessageBox.question(None, 'Message',
                                                   quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.hide()
                self.signal.emit(self)
