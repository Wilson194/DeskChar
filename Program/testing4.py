PersonSizeGraphicsItem::PersonSizeGraphicsItem(const QPixmap &pixmap, QGraphicsScene *scene)
    :QGraphicsPixmapItem(pixmap, 0, scene)
{
    this->setFlag(QGraphicsItem::ItemIsMovable, true);
    this->setFlag(QGraphicsItem::ItemIsSelectable, true);
    this->setFlag(QGraphicsItem::ItemSendsGeometryChanges, true);
    this->setFlag(QGraphicsItem::ItemIsFocusable, true);
    this->setFocus(Qt::MouseFocusReason);
    this->setAcceptHoverEvents(true);
    //this->setScale(0.5);

    rect_left_condition = false;
    rect_right_condition = false;
    rect_top_condition = false;
    rect_bottom_condition = false;
    rect_resize_occurred = false;
    image_rect = QRect();
    image_rect =  this->pixmap().toImage().rect();
}

void PersonSizeGraphicsItem::setSourceImage(const QImage& source_image)
{
    this->source_image =  source_image;
}


void PersonSizeGraphicsItem::mouseMoveEvent(QGraphicsSceneMouseEvent *event)
{
    const QPointF event_pos = event->pos();
    const QPointF event_scene_pos = event->scenePos();

    QPoint current_top_left = image_rect.topLeft();
    QPoint current_bottom_right = image_rect.bottomRight();

    if((event->scenePos().x() > this->scene()->width()) || (event->scenePos().y() > this->scene()->height())
        || (event->scenePos().x() < 0) || (event->scenePos().y() < 0) )
    {
        return;
    }

    if( this->cursor().shape() == Qt::SizeHorCursor )
    {
        if(rect_right_condition)
        {

        image_rect = QRect( current_top_left, QPoint( event->pos().x(), current_bottom_right.y()) );

        }

        if(rect_left_condition)
        {

            image_rect = QRect( QPoint(event_pos.x(), 0), current_bottom_right);

            QPoint new_top_left = image_rect.topLeft();
            QPointF mapped_topLeft = mapToParent(QPointF(new_top_left.x(),new_top_left.y()));
            this->setPos(mapped_topLeft);
            rect_resize_occurred = true;

            //qDebug() << "new rectangle top left**:" << this->pixmap().rect().topLeft();
        }

    }

    if( this->cursor().shape() == Qt::SizeVerCursor )
    {
        if(rect_bottom_condition)
        {

            image_rect = QRect(current_top_left, QPoint(current_bottom_right.x(), event->pos().y()));


    }

        if(rect_top_condition)
        {
            image_rect = QRect(QPoint(0, event_pos.y()), current_bottom_right);

                        QPoint new_top_left = image_rect.topLeft();
            QPointF mapped_topLeft = mapToParent(QPointF(new_top_left.x(),new_top_left.y()));
            this->setPos(mapped_topLeft);


        }
    }

    this->update();

}

void PersonSizeGraphicsItem::paint (QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    painter->drawImage(image_rect, source_image);
}