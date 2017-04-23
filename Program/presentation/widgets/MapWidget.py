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
from structure.map.MapItem import MapItem
from presentation.Translate import Translate as TR


class MapWidget(QtWidgets.QFrame):
    """
    Custom tab widget with function for editing templates
    """


    def __init__(self, parent, mainWindow):
        super().__init__(parent)

        self.mainWindow = mainWindow
        self.mapManager = MapManager()

        self.map = None

        self.init_bar()
        self.init_ui()


    def init_ui(self):
        """
        Init map widget UI
        :return: 
        """
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.frameLayout = QtWidgets.QVBoxLayout(self)
        self.frameLayout.setObjectName("Frame layout")

        self.grview = QGraphicsView()
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

        self.openMap_action = QAction(QIcon('resources/icons/open.png'), TR().tr('Open_map'), self.mainWindow,
                                      triggered=self.open_map_action, enabled=False)
        toolbar.addAction(self.openMap_action)

        self.zoomIn_action = QAction(QIcon('resources/icons/zoomIn.png'), TR().tr('Zoom_in'), self.mainWindow,
                                     triggered=self.zoom_in_action, shortcut='Ctrl++', enabled=False)
        toolbar.addAction(self.zoomIn_action)

        self.zoomOut_action = QAction(QIcon('resources/icons/zoomOut.png'), TR().tr('Zoom_out'), self.mainWindow,
                                      triggered=self.zoom_out_action, shortcut='Ctrl++', enabled=False)
        toolbar.addAction(self.zoomOut_action)

        self.add_action = QAction(QIcon('resources/icons/imp.png'), TR().tr('Add_monster'), self.mainWindow,
                                  triggered=self.add_item_action, shortcut='Ctrl+M', enabled=False)
        toolbar.addAction(self.add_action)

        self.save_action = QAction(QIcon('resources/icons/save.png'), TR().tr('Save'), self.mainWindow,
                                   triggered=self.save_action, shortcut='Ctrl+P', enabled=False)
        toolbar.addAction(self.save_action)


    def enable_tool_bar(self):
        self.openMap_action.setEnabled(True)
        self.zoomIn_action.setEnabled(True)
        self.zoomOut_action.setEnabled(True)
        self.add_action.setEnabled(True)
        self.save_action.setEnabled(True)


    def tree_item_doubleclick_action(self, item):
        self.enable_tool_bar()
        map = MapDAO().get(item.data(0, 11).id)
        if self.map:
            self.save_map()
        if self.map and self.map.id == map.id:
            map = MapDAO().get(item.data(0, 11).id)
        self.map = map
        self.redraw()


    def save_map(self):
        self.mapManager.update(self.map)


    def redraw(self):
        self.scene.clear()
        if self.map.mapFile:
            pixMap = QPixmap(self.map.mapFile)
            sceneMap = self.scene.addPixmap(pixMap)
            self.map.mapPixMap = sceneMap
            self.grview.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

        for mapItem in self.map.mapItems:
            item = MapItemDraw(mapItem)
            self.scene.addItem(item)
            self.map.addMapItemDraws(item)


    def open_map_action(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, "Open File",
                                                            QtCore.QDir.currentPath())

        if fileName:
            if self.map.mapPixMap:
                self.scene.removeItem(self.map.mapPixMap)

            self.map.mapFile = fileName
            self.map.mapPixMap = self.scene.addPixmap(QPixmap(fileName))
            self.grview.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)


    def zoom_in_action(self):
        self.grview.scale(1.2, 1.2)


    def zoom_out_action(self):
        self.grview.scale(0.8, 0.8)


    def add_item_action(self):
        mapItem = MapItem(None, None, None, QPointF(), 0, 15, None, self.map.id)
        id = MapItemDAO().create(mapItem)
        mapItem.id = id
        item = MapItemDraw(mapItem)
        self.scene.addItem(item)


    def save_action(self):
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

        img = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        img.fill(Qt.transparent)

        painter = QPainter(img)
        self.scene.render(painter)

        img.save('test.png')

        del painter


    def drawItems(self, painter, items, options, widget=None):
        pass


class MapItemDraw(QGraphicsPixmapItem):
    """
    Class for handling icon on scene
    """
    HANDLE_SIZE = 8


    def __init__(self, mapItem: MapItem):
        # Create backup of pixmap
        pix = QPixmap(mapItem.icon)
        self.oldPic = pix
        super().__init__(pix)

        self.mapItem = mapItem

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
