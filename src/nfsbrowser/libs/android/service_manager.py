import sys
from kivy.event import EventDispatcher
from jnius import autoclass

if sys.platform == "android":
    from android import mActivity

    Intent = autoclass("android.content.Intent")
    BuildVERSION = autoclass("android.os.Build$VERSION")
    JavaString = autoclass("java.lang.String")

registered_services = []


class ServiceManager(EventDispatcher):

    def __init__(self, **kwargs):
        super(ServiceManager, self).__init__(**kwargs)
        if sys.platform == "android":
            context = mActivity.getApplicationContext()
            self.package_name = str(context.getPackageName())

    def _get_service_class(self, nm):
        service_name = f"{self.package_name}.{nm}"
        try:
            service_class = autoclass(service_name)
            return service_class
        except Exception as e:
            print(f"Failed to load service class {service_name}: {e}")
            return None

    def start_service(self, nm, string_extras=None):
        """
        Starts the service.
        :param string_extras: A dictionary of extra string arguments (e.g., {"start_type": "START_STICKY"})
        """
        if sys.platform == "android":
            service_class = self._get_service_class(nm)
            if not service_class:
                print("Not found: ", nm)
                return

            print(f"Starting service {nm}")
            try:
                intent = Intent(mActivity, service_class)

                if string_extras and isinstance(string_extras, dict):
                    for key, value in string_extras.items():
                        intent.putExtra(JavaString(str(key)), JavaString(str(value)))

                # Android 8.0 (API 26) requires startForegroundService for background tasks
                if BuildVERSION.SDK_INT >= 26:
                    mActivity.startForegroundService(intent)
                else:
                    mActivity.startService(intent)

            except Exception as e:
                print(f"Error starting service {nm}: {e}")

            return service_class

    def stop_service(self, nm):
        if sys.platform == "android":
            service_class = self._get_service_class(nm)
            if not service_class:
                print("Not found: ", nm)
                return

            print(f"Stopped service {nm}")
            try:
                intent = Intent(mActivity, service_class)
                mActivity.stopService(intent)
            except Exception as e:
                print(f"Error stopping service {nm}: {e}")

    def restart_service(self, nm, string_extras=None):
        """
        Stops and then starts the service, passing any provided string extras along.
        """
        self.stop_service(nm)
        self.start_service(nm, string_extras=string_extras)
        print(f"Restarted service {nm}")

    def terminate_pool(self, *args) -> None:
        for service in registered_services:
            self.stop_service(service)


service_manager: ServiceManager = ServiceManager()
