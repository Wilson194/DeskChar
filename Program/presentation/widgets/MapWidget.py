from PyQt5 import QtWidgets, QtGui, QtCore
import numpy
import math

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap, QIcon
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, \
    QGraphicsItem, QAction, QGraphicsPixmapItem
from PyQt5.QtWidgets import QToolBar


class MapWidget(QtWidgets.QFrame):
    """
    Custom tab widget with function for editing templates
    """


    def __init__(self, parent, mainWindow):
        super().__init__(parent)

        self.mainWindow = mainWindow

        self.map = None

        self.init_bar()
        self.init_ui()


    def init_ui(self):
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.frameLayout = QtWidgets.QVBoxLayout(self)
        self.frameLayout.setObjectName("Frame layout")

        self.grview = QGraphicsView()
        self.scene = QGraphicsScene()

        # scene.setSceneRect(0, 0, 1500, 459)


        self.grview.setScene(self.scene)

        self.grview.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        self.frameLayout.addWidget(self.grview)


    def init_bar(self):
        toolbar = QToolBar()
        toolbar.setObjectName('MapToolbar')
        self.mainWindow.addToolBar(Qt.RightToolBarArea, toolbar)

        openMap_action = QAction(QIcon('resources/icons/open.png'), 'Zoom in', self.mainWindow,
                                 triggered=self.open_map_action)
        toolbar.addAction(openMap_action)

        zoomIn_action = QAction(QIcon('resources/icons/zoomIn.png'), 'Zoom in', self.mainWindow,
                                triggered=self.zoom_in_action, shortcut='Ctrl++')
        toolbar.addAction(zoomIn_action)

        zoomOut_action = QAction(QIcon('resources/icons/zoomOut.png'), 'Zoom out', self.mainWindow,
                                 triggered=self.zoom_out_action, shortcut='Ctrl++')
        toolbar.addAction(zoomOut_action)

        add_action = QAction(QIcon('resources/icons/imp.png'), 'Zoom out', self.mainWindow,
                             triggered=self.add_item_action, shortcut='Ctrl+M')
        toolbar.addAction(add_action)

        save_action = QAction(QIcon('resources/icons/save.png'), 'Save', self.mainWindow,
                              triggered=self.save_action, shortcut='Ctrl+P')
        toolbar.addAction(save_action)


    def open_map_action(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, "Open File",
                                                            QtCore.QDir.currentPath())

        if fileName:
            if self.map:
                self.scene.removeItem(self.map)

            self.map = self.scene.addPixmap(QPixmap(fileName))
            self.grview.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)


    def zoom_in_action(self):
        self.grview.scale(1.2, 1.2)


    def zoom_out_action(self):
        self.grview.scale(0.8, 0.8)


    def add_item_action(self):
        item = MapItem('resources/icons/imp.png', 15)
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


class MapItem(QGraphicsPixmapItem):
    HANDLE_SIZE = 8


    def __init__(self, iconPath, number):
        pix = QPixmap(iconPath)
        super().__init__(pix)

        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

        self.setZValue(50)
        self.topLeftHandle = None
        self.botRightHandle = None

        # self.oldPic = None

        self.oldPic = self.pixmap()
        self.resize = 0
        self.actualResize = 0

        self.number = number

        self.selectedHandle = None
        self.mousePressPos = None
        self.mousePressRect = None

        self.setAcceptHoverEvents(True)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)


    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

        font = painter.font()
        font.setPointSize(self.pixmap().height() / 6)
        painter.setFont(font)
        painter.drawText(self.boundingRect(), str(self.number))

        if self.isSelected():
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
            painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            s = self.HANDLE_SIZE
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

        s = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

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
