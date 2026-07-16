from jnius import autoclass, cast
from android.runnable import run_on_ui_thread  # type: ignore

PythonActivity = autoclass("org.kivy.android.PythonActivity")
View = autoclass("android.view.View")
ViewGroupLayoutParams = autoclass("android.widget.FrameLayout$LayoutParams")
Color = autoclass("android.graphics.Color")
Gravity = autoclass("android.view.Gravity")
ColorStateList = autoclass("android.content.res.ColorStateList")
ProgressBar = autoclass("android.widget.ProgressBar")

activity = PythonActivity.mActivity

_ACTIVE_LOADERS = {}

OverlayLayout = autoclass("android.widget.FrameLayout")


@run_on_ui_thread
def create_loader(loader_id: str = "default"):
    global _ACTIVE_LOADERS

    if loader_id in _ACTIVE_LOADERS:
        return

    overlay = OverlayLayout(activity)
    overlay.setClickable(True)
    overlay.setFocusable(True)
    overlay.setBackgroundColor(Color.parseColor("#00000000"))

    loader = ProgressBar(activity)
    loader.setIndeterminate(True)
    color_int = Color.parseColor("#0F62FE")
    loader.setIndeterminateTintList(ColorStateList.valueOf(color_int))

    params = ViewGroupLayoutParams(
        ViewGroupLayoutParams.WRAP_CONTENT, ViewGroupLayoutParams.WRAP_CONTENT
    )
    params.gravity = Gravity.CENTER
    overlay.addView(loader, params)

    full_params = ViewGroupLayoutParams(
        ViewGroupLayoutParams.MATCH_PARENT, ViewGroupLayoutParams.MATCH_PARENT
    )
    activity.addContentView(overlay, full_params)

    _ACTIVE_LOADERS[loader_id] = overlay


@run_on_ui_thread
def remove_loader(loader_id: str = "default"):
    global _ACTIVE_LOADERS
    loader = _ACTIVE_LOADERS.get(loader_id)

    if loader:
        parent = loader.getParent()
        if parent:
            real_parent = cast("android.view.ViewGroup", parent)
            real_parent.removeView(loader)

        del _ACTIVE_LOADERS[loader_id]
