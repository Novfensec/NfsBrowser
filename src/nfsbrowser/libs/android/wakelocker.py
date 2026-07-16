import logging
from jnius import autoclass, cast
from kivy.utils import platform

logger = logging.getLogger("WakeLocker")

if platform == "android":
    Context = autoclass("android.content.Context")
    PowerManager = autoclass("android.os.PowerManager")

    PythonService = autoclass("org.kivy.android.PythonService")
    app_context = PythonService.mService
    if app_context is None:
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        app_context = PythonActivity.mActivity
else:
    app_context = None


class WakeLocker:
    """
    An isolated API to manage Android WakeLocks.
    Default lock level is PARTIAL_WAKE_LOCK (keeps CPU running, allows screen to turn off).
    """

    def __init__(self, tag="AwferDriver::WakeLock", level="partial"):
        self.tag = tag
        self.wake_lock = None

        if platform != "android" or app_context is None:
            logger.warning("Not on Android or context is missing; WakeLock disabled.")
            return

        power_manager = cast(
            PowerManager, app_context.getSystemService(Context.POWER_SERVICE)
        )

        # Determine the lock level
        # PARTIAL_WAKE_LOCK = 1
        # ACQUIRE_CAUSES_WAKEUP = 268435456 (0x10000000)
        # SCREEN_BRIGHT_WAKE_LOCK = 10 (Deprecated in API 17, but still works for forced screen wakes)

        if level == "screen_bright":
            flags = (
                PowerManager.SCREEN_BRIGHT_WAKE_LOCK
                | PowerManager.ACQUIRE_CAUSES_WAKEUP
            )
        else:
            flags = PowerManager.PARTIAL_WAKE_LOCK

        self.wake_lock = power_manager.newWakeLock(flags, self.tag)

    def acquire(self, timeout_ms=None):
        """
        Acquire the wake lock.
        :param timeout_ms: Optional. If provided, the lock releases automatically after X milliseconds.
        """
        if self.wake_lock:
            try:
                if timeout_ms:
                    self.wake_lock.acquire(timeout_ms)
                    logger.debug(f"WakeLock '{self.tag}' acquired for {timeout_ms}ms.")
                else:
                    self.wake_lock.acquire()
                    logger.debug(f"WakeLock '{self.tag}' acquired indefinitely.")
            except Exception as e:
                logger.error(f"Failed to acquire WakeLock '{self.tag}': {e}")

    def release(self):
        """Release the wake lock safely."""
        if self.wake_lock and self.wake_lock.isHeld():
            try:
                self.wake_lock.release()
                logger.debug(f"WakeLock '{self.tag}' released.")
            except Exception as e:
                logger.error(f"Failed to release WakeLock '{self.tag}': {e}")

    def is_held(self):
        """Check if the lock is currently active."""
        if self.wake_lock:
            return self.wake_lock.isHeld()
        return False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
