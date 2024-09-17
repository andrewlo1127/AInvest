from PySide6.QtCore import QSize, Qt, QRectF
from PySide6.QtGui import QPainter, QImage, QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene


def set_blur_to_image(src: QImage, effect, extent: int = 0) -> QImage:
    """生成模糊图片"""
    if src.isNull():
        return QImage()
    if not effect:
        return src

    scene = QGraphicsScene()
    item = QGraphicsPixmapItem(QPixmap.fromImage(src))
    item.setGraphicsEffect(effect)
    scene.addItem(item)

    blur_image = QImage(src.size() + QSize(extent * 2, extent * 2), QImage.Format_ARGB32)
    blur_image.fill(Qt.transparent)

    painter = QPainter(blur_image)
    scene.render(painter, QRectF(), QRectF(-extent, -extent, src.width() + extent * 2, src.height() + extent * 2))
    painter.end()

    return blur_image
