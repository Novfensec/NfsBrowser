from android import mActivity
from android.runnable import run_on_ui_thread  # type: ignore
from android.permissions import Permission, request_permissions  # type: ignore
from jnius import autoclass

Build_VERSION = autoclass("android.os.Build$VERSION")
ContextCompat = autoclass("androidx.core.content.ContextCompat")
PackageManager = autoclass("android.content.pm.PackageManager")
sdk_int = Build_VERSION.SDK_INT

required_permissions = [
    Permission.FOREGROUND_SERVICE,
    Permission.ACCESS_COARSE_LOCATION,
    Permission.ACCESS_FINE_LOCATION,
    Permission.POST_NOTIFICATIONS,
]

if sdk_int >= 33:
    required_permissions.append(Permission.READ_MEDIA_IMAGES)
else:
    required_permissions.extend(
        [
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ]
    )

@run_on_ui_thread
def request_android_permissions(
    requested_permissions: list = required_permissions,
) -> None:
    print("Asking For Permissions")

    def callback(permissions, results):
        granted_permissions = [
            perm for perm, res in zip(permissions, results) if res
        ]
        denied_permissions = [
            perm for perm, res in zip(permissions, results) if not res
        ]

        if granted_permissions:
            print("Granted permissions:", granted_permissions)

        if denied_permissions:
            print("Denied permissions:", denied_permissions)

        if not granted_permissions and not denied_permissions:
            print("No permissions were granted or denied.")

    request_permissions(requested_permissions, callback)

def is_permission_granted(permissions: list[str]) -> bool:
    """
    Check if all given Android permissions are granted.

    Args:
        permissions (list[str]): List of Android permission strings

    Returns:
        bool: True if ALL are granted, False otherwise
    """

    for perm in permissions:
        result = ContextCompat.checkSelfPermission(mActivity, perm)
        if result != PackageManager.PERMISSION_GRANTED:
            return False
    return True
