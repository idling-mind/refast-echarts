"""Refast extension for ECharts

Provides the ECharts component for Refast applications.
"""

from pathlib import Path

from refast.extensions import Extension

from .components import ECharts, Echarts


class EchartsExtension(Extension):
    """
    ECharts extension for Refast.

    Provides Apache ECharts integration with support for all chart types,
    mouse events, theming, and dynamic updates via setOption.

    Example:
        ```python
        from refast import RefastApp, Context
        from refast_echarts import ECharts, EchartsExtension

        ui = RefastApp(extensions=[EchartsExtension()])

        @ui.page("/")
        def home(ctx: Context):
            return ECharts(
                id="my-chart",
                option={
                    "xAxis": {"data": ["A", "B", "C"]},
                    "yAxis": {},
                    "series": [{"type": "bar", "data": [10, 20, 30]}]
                },
                on_click=ctx.callback(handle_click),
                theme="light",
                height="400px",
            )
        ```

    For auto-discovery, install the package and it will be automatically loaded.
    """

    name = "refast-echarts"
    version = "0.1.0"
    description = "Refast extension for Apache ECharts"

    # Static assets to load (relative to static_path)
    scripts = ["refast-echarts.js"]
    styles = []  # ECharts doesn't require external CSS

    @property
    def static_path(self) -> Path:
        """Path to the static assets directory."""
        return Path(__file__).parent / "static"

    @property
    def components(self) -> list:
        """List of Python component classes provided by this extension."""
        return [ECharts]


__all__ = ["ECharts", "Echarts", "EchartsExtension"]
