import os
from jnius import autoclass, cast

# Android classes
Context = autoclass("android.content.Context")
NotificationManager = autoclass("android.app.NotificationManager")
NotificationChannel = autoclass("android.app.NotificationChannel")
NotificationCompatBuilder = autoclass("androidx.core.app.NotificationCompat$Builder")
BitmapFactory = autoclass("android.graphics.BitmapFactory")
BigPictureStyle = autoclass("androidx.core.app.NotificationCompat$BigPictureStyle")


PythonService = autoclass("org.kivy.android.PythonService")
service = PythonService.mService
if service == None:
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    service = PythonActivity.mActivity


def create_notification_channel():
    channel_id = "ch1"
    channel_name = "Messages"
    importance = NotificationManager.IMPORTANCE_HIGH

    channel = NotificationChannel(channel_id, channel_name, importance)
    channel.setDescription("Notifications for new messages")
    channel.enableVibration(True)
    channel.setShowBadge(True)

    manager = cast(
        NotificationManager, service.getSystemService(Context.NOTIFICATION_SERVICE)
    )
    manager.createNotificationChannel(channel)


def send_notification(title, body, img_path=None):
    builder = NotificationCompatBuilder(service, "ch1")
    builder.setSmallIcon(
        service.getResources().getIdentifier(
            "ic_launcher", "mipmap", service.getPackageName()
        )
    )
    builder.setContentTitle(title)
    builder.setContentText(body)
    builder.setAutoCancel(True)

    if img_path not in [None, "", "None"]:
        bitmap = BitmapFactory.decodeFile(img_path)
        style = BigPictureStyle().bigPicture(bitmap)
        builder.setStyle(style)

    notification = builder.build()
    manager = cast(
        NotificationManager, service.getSystemService(Context.NOTIFICATION_SERVICE)
    )
    manager.notify(1, notification)
