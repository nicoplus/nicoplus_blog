from app import create_celery_app

from app.extension import mail


celery = create_celery_app()


@celery.task(serializer='pickle')
def async_send_email(msg):
    mail.send(msg)
