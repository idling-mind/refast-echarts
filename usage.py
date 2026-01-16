"""
Comprehensive example usage of the ECharts component.

Demonstrates:
- Different chart types (bar, line, pie, scatter, radar, etc.)
- Mouse event handling (click, dblclick, hover, etc.)
- Dynamic updates via ctx.update_props and ctx.call_bound_js (setOption)
- Theming (light, dark)
- Auto-resize behavior
- Loading states

Run this file with:
    python usage.py

Then open http://localhost:8000 in your browser.
"""

import random
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import (
    Container, Card, CardHeader, CardTitle, CardContent, CardDescription,
    Text, Button, Row, Column, Select,
    Badge, Separator,
)

from refast_echarts import ECharts


ui = RefastApp(title="ECharts Demo - Comprehensive Examples")


# ============================================================================
# Event Handlers
# ============================================================================

async def handle_chart_click(ctx: Context):
    """Handle click events from charts."""
    data = ctx.event.data
    info = f"Clicked: {data.get('seriesName', 'N/A')} - {data.get('name', 'N/A')}: {data.get('value', 'N/A')}"
    print(f"[click] {info}")
    await ctx.update_text("event-info", info)


async def handle_chart_dblclick(ctx: Context):
    """Handle double-click events."""
    data = ctx.event.data
    info = f"Double-clicked: {data.get('name', 'N/A')}"
    print(f"[dblclick] {info}")
    await ctx.update_text("event-info", info)


async def handle_chart_hover(ctx: Context):
    """Handle mouseover events."""
    data = ctx.event.data
    if data.get('name'):
        info = f"Hovering: {data.get('name')}"
        await ctx.update_text("hover-info", info)


async def handle_chart_mouseout(ctx: Context):
    """Handle mouseout events."""
    await ctx.update_text("hover-info", "Hover over chart elements...")


# ============================================================================
# Update Functions
# ============================================================================

async def update_bar_chart_data(ctx: Context):
    """Update bar chart data using setOption via bound_js."""
    new_data = [random.randint(50, 300) for _ in range(7)]
    new_option = {
        "series": [{
            "data": new_data
        }]
    }
    await ctx.call_bound_js("bar-chart", "setOption", new_option)
    await ctx.update_text("event-info", f"Bar chart updated: {new_data}")


async def update_line_chart_data(ctx: Context):
    """Update line chart with new random data."""
    new_data1 = [random.randint(100, 500) for _ in range(7)]
    new_data2 = [random.randint(100, 500) for _ in range(7)]
    new_option = {
        "series": [
            {"data": new_data1},
            {"data": new_data2}
        ]
    }
    await ctx.call_bound_js("line-chart", "setOption", new_option)
    await ctx.update_text("event-info", "Line chart updated!")


async def update_pie_chart_data(ctx: Context):
    """Update pie chart with new random data."""
    categories = ["Electronics", "Clothing", "Food", "Books", "Other"]
    new_data = [{"name": cat, "value": random.randint(100, 500)} for cat in categories]
    new_option = {
        "series": [{
            "data": new_data
        }]
    }
    await ctx.call_bound_js("pie-chart", "setOption", new_option)
    await ctx.update_text("event-info", "Pie chart updated!")


async def toggle_loading(ctx: Context):
    """Toggle loading state on scatter chart."""
    await ctx.call_bound_js("scatter-chart", "showLoading", "default", {
        "text": "Loading data...",
        "color": "#3b82f6",
        "maskColor": "rgba(255, 255, 255, 0.8)"
    })
    # Simulate loading
    import asyncio
    await asyncio.sleep(2)
    await ctx.call_bound_js("scatter-chart", "hideLoading")
    await ctx.update_text("event-info", "Loading complete!")


async def clear_radar_chart(ctx: Context):
    """Clear the radar chart."""
    await ctx.call_bound_js("radar-chart", "clear")
    await ctx.update_text("event-info", "Radar chart cleared!")


async def restore_radar_chart(ctx: Context):
    """Restore radar chart with initial data."""
    radar_option = get_radar_option()
    await ctx.call_bound_js("radar-chart", "setOption", radar_option)
    await ctx.update_text("event-info", "Radar chart restored!")


# ============================================================================
# Chart Options
# ============================================================================

def get_bar_option():
    """Bar chart configuration."""
    return {
        "title": {
            "text": "Weekly Sales",
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"}
        },
        "legend": {
            "data": ["Sales"],
            "bottom": 0
        },
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        },
        "yAxis": {
            "type": "value"
        },
        "series": [{
            "name": "Sales",
            "type": "bar",
            "data": [120, 200, 150, 80, 70, 110, 130],
            "itemStyle": {
                "color": {
                    "type": "linear",
                    "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": "#3b82f6"},
                        {"offset": 1, "color": "#1d4ed8"}
                    ]
                }
            }
        }]
    }


def get_line_option():
    """Multi-line chart configuration."""
    return {
        "title": {
            "text": "Temperature Comparison",
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["New York", "London"],
            "bottom": 0
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {"formatter": "{value} °C"}
        },
        "series": [
            {
                "name": "New York",
                "type": "line",
                "data": [10, 11, 13, 11, 12, 12, 9],
                "smooth": True,
                "lineStyle": {"width": 3},
                "areaStyle": {"opacity": 0.3}
            },
            {
                "name": "London",
                "type": "line",
                "data": [1, -2, 2, 5, 3, 2, 0],
                "smooth": True,
                "lineStyle": {"width": 3},
                "areaStyle": {"opacity": 0.3}
            }
        ]
    }


def get_pie_option():
    """Pie/Donut chart configuration."""
    return {
        "title": {
            "text": "Sales by Category",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "top": "middle"
        },
        "series": [{
            "name": "Category",
            "type": "pie",
            "radius": ["40%", "70%"],  # Donut style
            "center": ["60%", "50%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2
            },
            "label": {
                "show": False,
                "position": "center"
            },
            "emphasis": {
                "label": {
                    "show": True,
                    "fontSize": 20,
                    "fontWeight": "bold"
                }
            },
            "labelLine": {"show": False},
            "data": [
                {"value": 1048, "name": "Electronics"},
                {"value": 735, "name": "Clothing"},
                {"value": 580, "name": "Food"},
                {"value": 484, "name": "Books"},
                {"value": 300, "name": "Other"}
            ]
        }]
    }


def get_scatter_option():
    """Scatter plot configuration."""
    # Generate random data points
    data1 = [[random.uniform(10, 90), random.uniform(10, 90)] for _ in range(50)]
    data2 = [[random.uniform(10, 90), random.uniform(10, 90)] for _ in range(50)]
    
    return {
        "title": {
            "text": "Correlation Analysis",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "({c})"
        },
        "legend": {
            "data": ["Dataset A", "Dataset B"],
            "bottom": 0
        },
        "xAxis": {
            "type": "value",
            "name": "X Axis"
        },
        "yAxis": {
            "type": "value",
            "name": "Y Axis"
        },
        "series": [
            {
                "name": "Dataset A",
                "type": "scatter",
                "data": data1,
                "symbolSize": 10,
                "itemStyle": {"color": "#3b82f6"}
            },
            {
                "name": "Dataset B",
                "type": "scatter",
                "data": data2,
                "symbolSize": 10,
                "itemStyle": {"color": "#ef4444"}
            }
        ]
    }


def get_radar_option():
    """Radar chart configuration."""
    return {
        "title": {
            "text": "Performance Metrics",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item"
        },
        "legend": {
            "data": ["Team A", "Team B"],
            "bottom": 0
        },
        "radar": {
            "indicator": [
                {"name": "Sales", "max": 100},
                {"name": "Marketing", "max": 100},
                {"name": "Development", "max": 100},
                {"name": "Support", "max": 100},
                {"name": "Innovation", "max": 100},
                {"name": "Quality", "max": 100}
            ],
            "center": ["50%", "55%"],
            "radius": "65%"
        },
        "series": [{
            "type": "radar",
            "data": [
                {
                    "value": [80, 90, 70, 85, 95, 75],
                    "name": "Team A",
                    "areaStyle": {"opacity": 0.3}
                },
                {
                    "value": [70, 75, 90, 70, 80, 90],
                    "name": "Team B",
                    "areaStyle": {"opacity": 0.3}
                }
            ]
        }]
    }


def get_gauge_option():
    """Gauge chart configuration."""
    return {
        "title": {
            "text": "System Health",
            "left": "center"
        },
        "tooltip": {
            "formatter": "{a} <br/>{b} : {c}%"
        },
        "series": [{
            "name": "Health",
            "type": "gauge",
            "center": ["50%", "60%"],
            "radius": "80%",
            "progress": {
                "show": True,
                "width": 18
            },
            "axisLine": {
                "lineStyle": {
                    "width": 18
                }
            },
            "axisTick": {"show": False},
            "splitLine": {
                "length": 15,
                "lineStyle": {
                    "width": 2,
                    "color": "#999"
                }
            },
            "axisLabel": {
                "distance": 25,
                "color": "#999",
                "fontSize": 12
            },
            "anchor": {
                "show": True,
                "showAbove": True,
                "size": 20,
                "itemStyle": {
                    "borderWidth": 8
                }
            },
            "detail": {
                "valueAnimation": True,
                "fontSize": 30,
                "offsetCenter": [0, "70%"],
                "formatter": "{value}%"
            },
            "data": [{
                "value": 78,
                "name": "CPU Usage"
            }]
        }]
    }


def get_heatmap_option():
    """Heatmap chart configuration."""
    hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a', '10a', '11a',
             '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p']
    days = ['Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon', 'Sun']
    
    # Generate random data for heatmap
    data = []
    for i in range(7):
        for j in range(24):
            data.append([j, i, random.randint(0, 10)])
    
    return {
        "title": {
            "text": "Weekly Activity Heatmap",
            "left": "center"
        },
        "tooltip": {
            "position": "top"
        },
        "grid": {
            "top": "15%",
            "bottom": "15%"
        },
        "xAxis": {
            "type": "category",
            "data": hours,
            "splitArea": {"show": True}
        },
        "yAxis": {
            "type": "category",
            "data": days,
            "splitArea": {"show": True}
        },
        "visualMap": {
            "min": 0,
            "max": 10,
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "0%"
        },
        "series": [{
            "type": "heatmap",
            "data": data,
            "label": {"show": False},
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }


# ============================================================================
# Page Definition
# ============================================================================

@ui.page("/")
def home(ctx: Context):
    """Home page with comprehensive ECharts examples."""
    
    return Container(
        class_name="max-w-7xl mx-auto py-8 px-4 space-y-8",
        children=[
            # Header
            Column(
                class_name="text-center space-y-2 mb-8",
                children=[
                    Text("ECharts Extension for Refast", class_name="text-3xl font-bold"),
                    Text(
                        "Interactive charts with full event support, theming, and dynamic updates",
                        class_name="text-muted-foreground text-lg"
                    ),
                ]
            ),
            
            # Event Info Bar
            Card(
                class_name="mb-6",
                children=[
                    CardContent(
                        class_name="py-4",
                        children=[
                            Row(
                                class_name="justify-between items-center gap-4 flex-wrap",
                                children=[
                                    Column(
                                        class_name="space-y-1",
                                        children=[
                                            Text("Event Info:", class_name="text-sm font-medium"),
                                            Text("Click on any chart element...", id="event-info", class_name="text-muted-foreground"),
                                        ]
                                    ),
                                    Column(
                                        class_name="space-y-1",
                                        children=[
                                            Text("Hover Info:", class_name="text-sm font-medium"),
                                            Text("Hover over chart elements...", id="hover-info", class_name="text-muted-foreground"),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            
            # Row 1: Bar and Line Charts
            Row(
                class_name="gap-6",
                children=[
                    # Bar Chart
                    Card(
                        class_name="flex-1",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Bar Chart"),
                                                    CardDescription("Click bars to see data, use button to randomize"),
                                                ]
                                            ),
                                            Badge("Interactive", variant="secondary"),
                                        ]
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    ECharts(
                                        id="bar-chart",
                                        option=get_bar_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        on_dblclick=ctx.callback(handle_chart_dblclick),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                    ),
                                    Button(
                                        "Randomize Data",
                                        on_click=ctx.callback(update_bar_chart_data),
                                        class_name="w-full"
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Line Chart
                    Card(
                        class_name="flex-1",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Line Chart"),
                                                    CardDescription("Multi-series with smooth lines and area fill"),
                                                ]
                                            ),
                                            Badge("Multi-Series", variant="secondary"),
                                        ]
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    ECharts(
                                        id="line-chart",
                                        option=get_line_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        on_mouseover=ctx.callback(handle_chart_hover),
                                        on_mouseout=ctx.callback(handle_chart_mouseout),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                    ),
                                    Button(
                                        "Update Data",
                                        on_click=ctx.callback(update_line_chart_data),
                                        class_name="w-full"
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            
            # Row 2: Pie and Scatter Charts
            Row(
                class_name="gap-6",
                children=[
                    # Pie Chart
                    Card(
                        class_name="flex-1",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Pie/Donut Chart"),
                                                    CardDescription("Donut style with emphasis label"),
                                                ]
                                            ),
                                            Badge("Animated", variant="secondary"),
                                        ]
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    ECharts(
                                        id="pie-chart",
                                        option=get_pie_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                    ),
                                    Button(
                                        "Randomize Values",
                                        on_click=ctx.callback(update_pie_chart_data),
                                        class_name="w-full"
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Scatter Chart
                    Card(
                        class_name="flex-1",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Scatter Plot"),
                                                    CardDescription("With loading state demo"),
                                                ]
                                            ),
                                            Badge("Loading Demo", variant="secondary"),
                                        ]
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    ECharts(
                                        id="scatter-chart",
                                        option=get_scatter_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                    ),
                                    Button(
                                        "Show Loading (2s)",
                                        on_click=ctx.callback(toggle_loading),
                                        class_name="w-full"
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            
            # Row 3: Radar and Gauge Charts
            Row(
                class_name="gap-6",
                children=[
                    # Radar Chart
                    Card(
                        class_name="flex-1",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Radar Chart"),
                                                    CardDescription("Performance comparison with clear/restore"),
                                                ]
                                            ),
                                            Badge("Clear/Restore", variant="secondary"),
                                        ]
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    ECharts(
                                        id="radar-chart",
                                        option=get_radar_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                    ),
                                    Row(
                                        class_name="gap-2",
                                        children=[
                                            Button(
                                                "Clear",
                                                on_click=ctx.callback(clear_radar_chart),
                                                variant="outline",
                                                class_name="flex-1"
                                            ),
                                            Button(
                                                "Restore",
                                                on_click=ctx.callback(restore_radar_chart),
                                                class_name="flex-1"
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Gauge Chart
                    Card(
                        class_name="flex-1",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Gauge Chart"),
                                                    CardDescription("System health indicator"),
                                                ]
                                            ),
                                            Badge("Progress", variant="secondary"),
                                        ]
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    ECharts(
                                        id="gauge-chart",
                                        option=get_gauge_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="350px",
                                        theme="light",
                                        auto_resize=True,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            
            # Row 4: Heatmap (Full Width)
            Card(
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Heatmap Chart"),
                                            CardDescription("Weekly activity visualization with visual mapping"),
                                        ]
                                    ),
                                    Badge("Full Width", variant="secondary"),
                                ]
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            ECharts(
                                id="heatmap-chart",
                                option=get_heatmap_option(),
                                on_click=ctx.callback(handle_chart_click),
                                height="350px",
                                theme="light",
                                auto_resize=True,
                            ),
                        ]
                    ),
                ]
            ),
            
            # Dark Theme Example
            Card(
                class_name="bg-slate-900",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Dark Theme Example", class_name="text-white"),
                                            CardDescription("Same bar chart with dark theme", class_name="text-slate-400"),
                                        ]
                                    ),
                                    Badge("theme='dark'", variant="outline", class_name="text-white border-slate-600"),
                                ]
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            ECharts(
                                id="dark-chart",
                                option=get_bar_option(),
                                on_click=ctx.callback(handle_chart_click),
                                height="300px",
                                theme="dark",
                                auto_resize=True,
                            ),
                        ]
                    ),
                ]
            ),
            
            # Footer
            Separator(),
            Column(
                class_name="text-center space-y-2 py-4",
                children=[
                    Text("ECharts Extension for Refast", class_name="font-medium"),
                    Text(
                        "Supports all ECharts chart types • Mouse events • Theming • Dynamic updates via setOption",
                        class_name="text-sm text-muted-foreground"
                    ),
                ]
            ),
        ]
    )


# Create FastAPI app
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

