# -*- coding:utf-8 -*-
import sys
import os
import copy
import time
import glob
from PySide2 import QtGui, QtCore, QtWidgets

'''
◆環境
 macOS version 10.15~
 python 3.7.6
 PySide2 5.14.1
'''

username = os.getlogin()
__TESTICONS__ = '/Users/%s/Pictures/screenshot.jpg'%username # Imageディレクトリ
#========================================================================================
class PoQListWidget(QtWidgets.QListWidget):
    ''' ドラッグアンドドロップ実行用の為の関数 '''
    def __init__( self, parent ):
        super( PoQListWidget, self ).__init__(  )
        self.setParent(parent)
    
    #---------------------------------------------------------------------
    def startDrag(self, dropAction):
        ''' mimeをドロップ先に渡す為の設定を行う関数。 '''
        # create mime data object
        print('startDrag')
        mime = QtCore.QMimeData()
        #mime.setUrls(['test','popo'])
        #mime.setData('application/x-item', '???')
        mime.setText(self.selectedItems()[0].metaData)
        mime.tempData =self.selectedItems()[0].icon().pixmap(100, 100)
        #mime.setPixmap()
        # start drag
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)
        drag.start(QtCore.Qt.CopyAction | QtCore.Qt.CopyAction)


#========================================================================================
class ExObject():
    ''' ItemMangerで実行する '''
    def __init__(self):
        pass
    def execute(self):
        print('execute')


#========================================================================================
class ScreenShot( QtWidgets.QWidget ):
    ''' スクリーショット用クラス '''
    def __init__( self, arg ):
        super( ScreenShot, self ).__init__( )
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.label=QtWidgets.QLabel(self)
        #self.button = QtWidgets.QPushButton('test', parent=self)
        #self.button.clicked.connect(self.shot)
        self.widget=arg
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setGeometry(QtWidgets.QApplication.desktop().geometry())
        
        self.painter = QtGui.QPainter(self)
        self.layout().addWidget(self.label)
        #self.layout().addWidget(self.button)
        
        self.setBackgroundColor()
        #self.setBackgroundColor(self.QGview, color=(30, 30, 40, 0))
        
        self._startPos = None
        self._currentPos = None
    
    #-----------------------------------------------------------------
    def settingPainter(self):
        ''' QPainterの設定 '''
        self.pen = QtGui.QPen()
        ##self.pen.setStyle(QtCore.Qt.DashDotLine)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.pen.setWidth(3)
        self.pen.setBrush(QtCore.Qt.red)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.painter.setPen(self.pen)
    
    #-----------------------------------------------------------------
    def paintEvent(self, event):
        ''' スクリーンショット用枠の表示 '''
        self.painter.begin(self)
        self.settingPainter()
        
        if (self._startPos !=None) and (self._currentPos !=None):
            self.painter.drawLine(self._startPos.x(), self._startPos.y(), self._currentPos.x(), self._startPos.y())
            self.painter.drawLine(self._currentPos.x(), self._startPos.y(), self._currentPos.x(), self._currentPos.y())
            self.painter.drawLine(self._startPos.x(), self._startPos.y(), self._startPos.x(), self._currentPos.y())
            self.painter.drawLine(self._startPos.x(), self._currentPos.y(), self._currentPos.x(), self._currentPos.y())
        self.painter.end()
    
    #-----------------------------------------------------------------
    def shot(self):
        ''' スクリーンショット保存 '''
        print('shot')
        penPixel = 4
        stPos = self._startPos
        enPos = self._currentPos
        st_x, st_y = stPos.x(), stPos.y()
        en_x, en_y = enPos.x(), enPos.y()
        print(st_x, st_y, en_x, en_y)
        # 上下逆の場合の入れ替え ※入れ替えの仕様違いに注意
        if st_x > en_x:
            st_x, en_x=en_x, st_x
        if st_y > en_y:
            st_y, en_y=en_y, st_y
            
        stPos = QtCore.QPoint(st_x+penPixel, st_y+penPixel)
        enPos = QtCore.QPoint(en_x-penPixel, en_y-penPixel)
        
        pos_gst = self.mapToGlobal(stPos)
        size = enPos-stPos
        id = QtWidgets.QApplication.desktop().winId()
        p = QtGui.QPixmap.grabWindow(id, pos_gst.x(), pos_gst.y(), size.x(), size.y())
        username = os.getlogin()
        print(p.save('/Users/%s/Pictures/screenshot.jpg'%username, 'jpg'))
        print("== save ==")
        #self.label.setPixmap(p)
        #time.sleep(0.01)
        #self.button.hide()
        #self.label.show()
        #self.show()
    
    #-----------------------------------------------------------------
    def mousePressEvent(self, event):
        ''' スクリーンショット用外枠表示開始点設定 '''
        self._startPos = event.pos()
        #self.QGscene.addText("Hello, world!");
    
    #-----------------------------------------------------------------
    def mouseMoveEvent(self, event):
        ''' スクリーンショット用外枠表示 '''
        position = event.pos()
        self._currentPos = position
        self.update()
    
    #-----------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        ''' マウスボタンを離した際にスクリーンショット実行 '''
        button = event.button()
        if button == QtCore.Qt.LeftButton:
            position = event.pos()
            self._currentPos = position
            self.update()
            self.shot()
        elif button == QtCore.Qt.RightButton:
            self.close()
        
            
    #-----------------------------------------------------------------
    def setBackgroundColor(self, arg=None, color=(30, 30, 40, 0)):
        ''' 背景色を設定。 '''
        if arg is None:
            arg = self
        p = arg.palette()
        p.setColor(arg.backgroundRole(), QtGui.QColor(*color))
        arg.setPalette(p)


#========================================================================================
class ItemManager():
    ''' pixmapと関連付けし関数を実行する為のマネージャー '''
    def __init__( self ):
        self.itemDic = {}
    
    def setItem( self, keyitem ):
        self.itemDic.update({keyitem:ExObject() })
    
    def getItem( self, keyitem ):
        print(keyitem, self.itemDic[str(keyitem)])
        return self.itemDic[str(keyitem)]


#========================================================================================
class ItemViewer( QtWidgets.QGraphicsView ):
    ''' itemをワークスペースに設定する為の観覧用QListWidget '''
    def __init__( self ):
        super( ItemViewer, self ).__init__( )
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.listwidget = PoQListWidget(self)#QtWidgets.QListWidget(self)
        self.listwidget.setGeometry(30, 40, 500, 300)
        self.listwidget.setViewMode( self.listwidget.IconMode )
        self.listwidget.setGridSize( QtCore.QSize(50,50) )
        self.layout().addWidget(self.listwidget)
    
    #-----------------------------------------------------------------
    def setTestItems( self ):
        ''' テスト用アイテム設定関数 '''
        imagepath = __TESTICONS__
        self.pixmapItems =[]
        print(imagepath+'/*')
        for num, i in enumerate(glob.glob(imagepath)):
            print(i)
            tempPixmap = QtGui.QPixmap(i)
            tempIcon = QtGui.QIcon(tempPixmap)
            tempItem = QtWidgets.QListWidgetItem()
            tempItem.setIcon(tempIcon)
            tempItem.metaData = i
            tempPixmap.metaData = i
            self.setItem_inManager(i)
            self.listwidget.addItem(tempItem)
                
    #-----------------------------------------------------------------
    def addItem(self, metaData, filePath, imagepath=__TESTICONS__):
        '''  metaData iconFilaPathからlistWidgetItemを追加 '''
        import glob
        self.pixmapItems =[]
        files = []
        types = ['png', 'jpg', 'gif', 'tiff', 'tga']
        for t in types:
            path = '%s/*.%s'%(imagepath, t)
            files += glob.glob(path)
        for num, i in enumerate():
            tempPixmap = QtGui.QPixmap(i)
            tempIcon = QtGui.QIcon(tempPixmap)
            tempItem = QtWidgets.QListWidgetItem()
            tempItem.setIcon(tempIcon)
            tempItem.metaData = i
            tempPixmap.metaData = i
            self.setItem_inManager(i)
            self.listwidget.addItem(tempItem)

    #-----------------------------------------------------------------
    def getItem_fromManager( self, arg ):
        ''' 設定したitemManagerからitemを取得。キーにはpixmapを使用。 '''
        self.iManager.getItem(arg)

    #-----------------------------------------------------------------
    def setItemManager( self, arg ):
        ''' itemをpixmapから使用/設定する為のitemManagerを設定。 '''
        self.iManager = arg
    
    #-----------------------------------------------------------------
    def setItem_inManager( self, pixmap ):
        ''' 設定したitemManagerから取得。キーにはpixmapを使用。 '''
        self.iManager.setItem(pixmap)

    #-----------------------------------------------------------------
    def setBackgroundColor(self, arg=None):
        ''' 背景色を設定。 '''
        if arg is None:
            arg = self
        p = arg.palette()
        p.setColor(arg.backgroundRole(), QtGui.QColor(30, 30, 40))
        arg.setPalette(p)


#========================================================================================
class ImageViewer( QtWidgets.QGraphicsView ):
    ''' ワークスペース用のイメージビュワー '''
    def __init__( self ):
        super( ImageViewer, self ).__init__( )
        
        self.setCacheMode( QtWidgets.QGraphicsView.CacheBackground )
        self.setRenderHints( QtGui.QPainter.Antialiasing |
                            QtGui.QPainter.SmoothPixmapTransform |
                            QtGui.QPainter.TextAntialiasing
                            )

        self.QGscene = QtWidgets.QGraphicsScene()
        self.sceneSize = 100
        self.pixmapItems =[]
        self.setBackgroundColor()
        #Qpainted = QtGui.QPainter()
        #Qpainted.fillRect(0, 0, 1000, 100, QtGui.QColor(30, 30, 40))
        #self.QGscene.drawBackground(Qpainted, QtCore.QRectF(1, 1, 100, 200))
        
        self.setAcceptDrops(True)
        
        self.setScene(self.QGscene)
        #self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self._scale = 1.0
        #self.setInteractive(True)
        #self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        #self.setViewportUpdateMode(QtWidgets.QGraphicsView.MinimalViewportUpdate)
    
    
    #---------------------------------------------------------------------
    def mouseDoubleClickEvent( self, event ):
        ''' ダブルクリック時に選択中のアイテムからitemManagerを用いて関数を実行、または取得。 '''
        pos = self.mapToScene(event.pos())
        for i in self.pixmapItems:
            if i.isSelected():
                print(i.metaData)
                self.getItem_fromManager(i.metaData)
                print(i.pos())

    #---------------------------------------------------------------------
    def dragEnterEvent( self, event ):
        ''' dropイベント用ダミー。 '''
        print('enter')
        event.accept()
    
    #---------------------------------------------------------------------
    def addItems( self, imagefile=None, position=[0,0] ):
        ''' QGraphicシーンにpixmapをイメージファイルパスを用いて追加。 '''
        tempPixmap = QtGui.QPixmap(imagefile)
        tempPixmap = self.QGscene.addPixmap(tempPixmap)
        tempPixmap.oPosition = position
        tempPixmap.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsSelectable )
        self.pixmapItems.append(tempPixmap)
    
    #---------------------------------------------------------------------
    def addPixmap( self, pixmap=None, position=[0,0], metaData=None ):
        ''' QGraphicシーンにpixmapを追加。'''
        print(self.QGscene)
        tempPixmap = self.QGscene.addPixmap(pixmap)
        tempPixmap.oPosition = position
        tempPixmap.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable )
        tempPixmap.metaData =metaData
        tempPixmap.setPos(*position)
        self.pixmapItems.append(tempPixmap)
    
    #---------------------------------------------------------------------
    #
    def dropEvent( self, event ):
        ''' ドロップイベント設定。受け取ったmimeからドロップ時のマウス位置にmimeに設定されたpixmapを追加。 '''
        #self.scene().clear()
        pos = self.mapToScene(event.pos())
        print(pos)
        pos = (float(pos.x()), float(pos.y()))
        print(pos)
        print( 'drop')
        mimedata= event.mimeData()
        print(mimedata.text())
        print(event.mimeData().data("application/x-item"))
        #print(mindata.formats().takeAt(1))
        print(event.mimeData().urls())
        print(mimedata.tempData)
        pximap = QtGui.QPixmap(mimedata.text())
        iconpixmap = mimedata.tempData
        self.addPixmap(pximap, pos, mimedata.text())
    
    #-----------------------------------------------------------------
    def dragMoveEvent( self, event ):
        ''' ドロップイベント '''
        print('drag')
    
    #-----------------------------------------------------------------
    def wheelEvent( self, event ):
        ''' マウスホイールが縦に使用された場合のシーンのスケール処理。 '''
        scaleFactor =0.001
        if event.orientation()==2:
            currentScale = self._scale +(event.delta()*scaleFactor)
            #self._scale = currentScale
            self.scale( currentScale, currentScale )

    #-----------------------------------------------------------------
    def getItem_fromManager( self, arg ):
        ''' 設定したitemManagerからitemを取得。キーにはpixmapを使用。 '''
        self.iManager.getItem(arg)
    
    #-----------------------------------------------------------------
    def setItemManager( self, arg ):
        ''' itemをpixmapから使用する為のitemManagerを設定。 '''
        self.iManager = arg
    
    #-----------------------------------------------------------------
    def setBackgroundColor(self, arg=None):
        ''' 背景色を設定。 '''
        if arg is None:
            arg = self
        p = arg.palette()
        p.setColor(arg.backgroundRole(), QtGui.QColor(40, 40, 50))
        arg.setPalette(p)

#========================================================================================

# ---------------------------------------------------------------------
# テスト実行
if __name__ == '__main__':
    app = QtWidgets.QApplication( sys.argv )
    class MainWidget(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super(MainWidget, self).__init__(parent)
            self.setLayout(QtWidgets.QHBoxLayout(self))
            
            self._menubar = QtWidgets.QMenuBar()
            menu = self._menubar.addMenu("Menu")
            action = menu.addAction("ScreenShot")
            action.triggered.connect(self.start_screenshot)

            self.__itemManager=ItemManager()
            self._viewer = ImageViewer()
            self._viewer.setItemManager(self.__itemManager)
            self.hogettest = ItemViewer()
            self.hogettest.setItemManager(self.__itemManager)
            self.hogettest.setTestItems()
            
            self.layout().addWidget(self._menubar)
            self.layout().addWidget(self.hogettest)
            self.layout().addWidget(self._viewer)
            self.resize(1200, 498)
            
        
        def start_screenshot(self):
            self._screenshot = ScreenShot(self);
            self._screenshot.show()
    
    hoge = MainWidget()
    hoge.show()
    
    sys.exit( app.exec_() )
