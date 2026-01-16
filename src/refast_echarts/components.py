"""Component definitions for Refast extension for ECharts."""

from typing import Any, Literal

from refast.components.base import Component
from refast.components.registry import register_component


@register_component(
    name="ECharts",
    package="refast-echarts",
    module="components",
)
class ECharts(Component):
    """
    Apache ECharts component for Refast.
    
    A powerful charting library that supports many chart types including
    line, bar, pie, scatter, candlestick, map, and more.
    
    Args:
        option: ECharts option configuration object.
        theme: Theme name ('light', 'dark') or custom theme object.
        init_opts: Initialization options for ECharts instance.
        auto_resize: Whether to auto-resize chart when container size changes (default True).
        width: Chart width (e.g., "100%", "600px"). If None, uses container width.
        height: Chart height (e.g., "400px"). If None, uses container height.
        loading: Whether to show loading animation.
        loading_opts: Loading animation options.
        
        Event callbacks (all receive event data with chart interaction details):
        on_click: Fired when clicking on a chart element.
        on_dblclick: Fired when double-clicking on a chart element.
        on_mousedown: Fired on mouse down.
        on_mousemove: Fired on mouse move.
        on_mouseup: Fired on mouse up.
        on_mouseover: Fired when hovering over a chart element.
        on_mouseout: Fired when mouse leaves a chart element.
        on_globalout: Fired when mouse leaves the chart area entirely.
        on_contextmenu: Fired on right-click context menu.
        
        id: Component ID (required for bound_js calls like setOption).
        class_name: CSS classes to apply to the container.
        style: Inline styles for the container.
    
    Bound Methods (callable via ctx.bound_js() or ctx.call_bound_js()):
        setOption(option, notMerge=False, lazyUpdate=False): Update chart options.
        resize(opts=None): Resize the chart.
        clear(): Clear the chart.
        showLoading(type='default', opts=None): Show loading animation.
        hideLoading(): Hide loading animation.
        getDataURL(opts=None): Get chart image as data URL.
        dispose(): Dispose the chart instance.
    
    Example:
        ```python
        from refast import RefastApp, Context
        from refast_echarts import ECharts
        
        ui = RefastApp()
        
        async def handle_click(ctx: Context):
            data = ctx.event.data
            print(f"Clicked: {data.get('name')}: {data.get('value')}")
        
        async def update_chart(ctx: Context):
            new_option = {
                "series": [{"data": [100, 200, 150, 80, 70]}]
            }
            await ctx.call_bound_js("my-chart", "setOption", new_option)
        
        @ui.page("/")
        def home(ctx: Context):
            return ECharts(
                id="my-chart",
                option={
                    "title": {"text": "Sales Chart"},
                    "xAxis": {"data": ["Mon", "Tue", "Wed", "Thu", "Fri"]},
                    "yAxis": {},
                    "series": [{"type": "bar", "data": [120, 200, 150, 80, 70]}]
                },
                on_click=ctx.callback(handle_click),
                theme="light",
                height="400px",
            )
        ```
    """
    
    component_type = "ECharts"

    def __init__(
        self,
        option: dict[str, Any] | None = None,
        theme: str | dict[str, Any] | None = None,
        init_opts: dict[str, Any] | None = None,
        auto_resize: bool = True,
        width: str | None = None,
        height: str | None = None,
        loading: bool = False,
        loading_opts: dict[str, Any] | None = None,
        # Mouse event callbacks
        on_click: Any = None,
        on_dblclick: Any = None,
        on_mousedown: Any = None,
        on_mousemove: Any = None,
        on_mouseup: Any = None,
        on_mouseover: Any = None,
        on_mouseout: Any = None,
        on_globalout: Any = None,
        on_contextmenu: Any = None,
        # Base props
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.option = option or {}
        self.theme = theme
        self.init_opts = init_opts
        self.auto_resize = auto_resize
        self.width = width
        self.height = height
        self.loading = loading
        self.loading_opts = loading_opts
        self.style = style or {}
        
        # Event callbacks
        self.on_click = on_click
        self.on_dblclick = on_dblclick
        self.on_mousedown = on_mousedown
        self.on_mousemove = on_mousemove
        self.on_mouseup = on_mouseup
        self.on_mouseover = on_mouseover
        self.on_mouseout = on_mouseout
        self.on_globalout = on_globalout
        self.on_contextmenu = on_contextmenu

    def _serialize_callback(self, callback: Any) -> dict | None:
        """Serialize a callback if present."""
        if callback is None:
            return None
        if hasattr(callback, 'serialize'):
            return callback.serialize()
        return callback

    def render(self) -> dict[str, Any]:
        # Build style dict, applying width/height if specified
        computed_style = {**self.style}
        if self.width:
            computed_style["width"] = self.width
        if self.height:
            computed_style["height"] = self.height
        
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "option": self.option,
                "theme": self.theme,
                "init_opts": self.init_opts,
                "auto_resize": self.auto_resize,
                "loading": self.loading,
                "loading_opts": self.loading_opts,
                "style": computed_style if computed_style else None,
                "class_name": self.class_name,
                # Event callbacks
                "on_click": self._serialize_callback(self.on_click),
                "on_dblclick": self._serialize_callback(self.on_dblclick),
                "on_mousedown": self._serialize_callback(self.on_mousedown),
                "on_mousemove": self._serialize_callback(self.on_mousemove),
                "on_mouseup": self._serialize_callback(self.on_mouseup),
                "on_mouseover": self._serialize_callback(self.on_mouseover),
                "on_mouseout": self._serialize_callback(self.on_mouseout),
                "on_globalout": self._serialize_callback(self.on_globalout),
                "on_contextmenu": self._serialize_callback(self.on_contextmenu),
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


# Alias for backward compatibility
Echarts = ECharts