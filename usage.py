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
    Container,
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    CardDescription,
    Text,
    Button,
    Row,
    Column,
    Badge,
    Separator,
    ThemeSwitcher,
)

from refast_echarts import ECharts


ui = RefastApp(title="ECharts Demo - Comprehensive Examples")


# ============================================================================
# Event Handlers
# ============================================================================


async def handle_chart_click(ctx: Context):
    """Handle click events from charts."""
    data = ctx.event_data
    info = f"Clicked: {data.get('seriesName', 'N/A')} - {data.get('name', 'N/A')}: {data.get('value', 'N/A')}"
    print(f"[click] {info}")
    await ctx.append("event-info", Text(info, class_name="block"))
    # await ctx.update_text("event-info", info)


async def handle_chart_dblclick(ctx: Context):
    """Handle double-click events."""
    data = ctx.event_data
    info = f"Double-clicked: {data.get('name', 'N/A')}"
    print(f"[dblclick] {info}")
    await ctx.update_text("event-info", info)


async def handle_chart_hover(ctx: Context):
    """Handle mouseover events."""
    data = ctx.event_data
    if data.get("name"):
        info = f"Hovering: {data.get('name')}"
        await ctx.update_text("hover-info", info)


async def handle_chart_mouseout(ctx: Context):
    """Handle mouseout events."""
    await ctx.update_text("hover-info", "Hover over chart elements...")


async def theme_switched(ctx: Context):
    """Handle theme switcher changes."""
    new_theme = ctx.event_data["value"]  # 'light' or 'dark'
    print(f"[theme switched] New theme: {new_theme}")
    for chart in [
        "bar-chart",
        "line-chart",
        "pie-chart",
        "nightingale-chart",
        "scatter-chart",
        "radar-chart",
        "gauge-chart",
        "heatmap-chart",
        "sankey-chart",
    ]:
        await ctx.update_props(chart, {"theme": new_theme})
    await ctx.update_text("event-info", f"Theme switched to: {new_theme}")


# ============================================================================
# Update Functions
# ============================================================================


async def update_bar_chart_data(ctx: Context):
    """Update bar chart data using setOption via bound_js."""
    new_data = [random.randint(50, 300) for _ in range(7)]
    new_option = {"series": [{"data": new_data}]}
    await ctx.call_bound_js("bar-chart", "setOption", new_option)
    await ctx.update_text("event-info", f"Bar chart updated: {new_data}")


async def update_line_chart_data(ctx: Context):
    """Update line chart with new random data."""
    new_data1 = [random.randint(100, 500) for _ in range(7)]
    new_data2 = [random.randint(100, 500) for _ in range(7)]
    new_option = {"series": [{"data": new_data1}, {"data": new_data2}]}
    await ctx.update_props("line-chart", {"option": new_option})
    await ctx.update_text("event-info", "Line chart updated!")


async def update_pie_chart_data(ctx: Context):
    """Update pie chart with new random data."""
    categories = ["Electronics", "Clothing", "Food", "Books", "Other"]
    new_data = [{"name": cat, "value": random.randint(100, 500)} for cat in categories]
    new_option = {"series": [{"data": new_data}]}
    await ctx.call_bound_js("pie-chart", "setOption", new_option)
    await ctx.update_text("event-info", "Pie chart updated!")


async def toggle_loading(ctx: Context):
    """Toggle loading state on scatter chart."""
    await ctx.call_bound_js(
        "scatter-chart",
        "showLoading",
        "default",
        {
            "text": "Loading data...",
            "color": "#3b82f6",
            "maskColor": "rgba(255, 255, 255, 0.8)",
        },
    )
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
        "title": {"text": "Weekly Sales", "left": "center"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": ["Sales"], "bottom": 0},
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Sales",
                "type": "bar",
                "data": [120, 200, 150, 80, 70, 110, 130],
                "itemStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0,
                        "y": 0,
                        "x2": 0,
                        "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "#3b82f6"},
                            {"offset": 1, "color": "#1d4ed8"},
                        ],
                    }
                },
            }
        ],
    }


def get_line_option():
    """Multi-line chart configuration."""
    return {
        "title": {"text": "Temperature Comparison", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["New York", "London"], "bottom": 0},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value", "axisLabel": {"formatter": "{value} °C"}},
        "series": [
            {
                "name": "New York",
                "type": "line",
                "data": [10, 11, 13, 11, 12, 12, 9],
                "smooth": True,
                "lineStyle": {"width": 3},
                "areaStyle": {"opacity": 0.3},
            },
            {
                "name": "London",
                "type": "line",
                "data": [1, -2, 2, 5, 3, 2, 0],
                "smooth": True,
                "lineStyle": {"width": 3},
                "areaStyle": {"opacity": 0.3},
            },
        ],
    }


def get_pie_option():
    """Pie/Donut chart configuration."""
    return {
        "title": {"text": "Sales by Category", "left": "center"},
        "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b}: {c} ({d}%)"},
        "legend": {"orient": "vertical", "left": "left", "top": "middle"},
        "series": [
            {
                "name": "Category",
                "type": "pie",
                "radius": ["40%", "70%"],  # Donut style
                "center": ["60%", "50%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": 20, "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": [
                    {"value": 1048, "name": "Electronics"},
                    {"value": 735, "name": "Clothing"},
                    {"value": 580, "name": "Food"},
                    {"value": 484, "name": "Books"},
                    {"value": 300, "name": "Other"},
                ],
            }
        ],
    }


def get_scatter_option():
    """Scatter plot configuration."""
    # Generate random data points
    data1 = [[random.uniform(10, 90), random.uniform(10, 90)] for _ in range(50)]
    data2 = [[random.uniform(10, 90), random.uniform(10, 90)] for _ in range(50)]

    return {
        "title": {"text": "Correlation Analysis", "left": "center"},
        "tooltip": {"trigger": "item", "formatter": "({c})"},
        "legend": {"data": ["Dataset A", "Dataset B"], "bottom": 0},
        "xAxis": {"type": "value", "name": "X Axis"},
        "yAxis": {"type": "value", "name": "Y Axis"},
        "series": [
            {
                "name": "Dataset A",
                "type": "scatter",
                "data": data1,
                "symbolSize": 10,
                "itemStyle": {"color": "#3b82f6"},
            },
            {
                "name": "Dataset B",
                "type": "scatter",
                "data": data2,
                "symbolSize": 10,
                "itemStyle": {"color": "#ef4444"},
            },
        ],
    }


def get_radar_option():
    """Radar chart configuration."""
    return {
        "title": {"text": "Performance Metrics", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"data": ["Team A", "Team B"], "bottom": 0},
        "radar": {
            "indicator": [
                {"name": "Sales", "max": 100},
                {"name": "Marketing", "max": 100},
                {"name": "Development", "max": 100},
                {"name": "Support", "max": 100},
                {"name": "Innovation", "max": 100},
                {"name": "Quality", "max": 100},
            ],
            "center": ["50%", "55%"],
            "radius": "65%",
        },
        "series": [
            {
                "type": "radar",
                "data": [
                    {
                        "value": [80, 90, 70, 85, 95, 75],
                        "name": "Team A",
                        "areaStyle": {"opacity": 0.3},
                    },
                    {
                        "value": [70, 75, 90, 70, 80, 90],
                        "name": "Team B",
                        "areaStyle": {"opacity": 0.3},
                    },
                ],
            }
        ],
    }


def get_gauge_option():
    """Gauge chart configuration."""
    return {
        "title": {"text": "System Health", "left": "center"},
        "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
        "series": [
            {
                "name": "Health",
                "type": "gauge",
                "center": ["50%", "60%"],
                "radius": "80%",
                "progress": {"show": True, "width": 18},
                "axisLine": {"lineStyle": {"width": 18}},
                "axisTick": {"show": False},
                "splitLine": {"length": 15, "lineStyle": {"width": 2, "color": "#999"}},
                "axisLabel": {"distance": 25, "color": "#999", "fontSize": 12},
                "anchor": {
                    "show": True,
                    "showAbove": True,
                    "size": 20,
                    "itemStyle": {"borderWidth": 8},
                },
                "detail": {
                    "valueAnimation": True,
                    "fontSize": 30,
                    "offsetCenter": [0, "70%"],
                    "formatter": "{value}%",
                },
                "data": [{"value": 78, "name": "CPU Usage"}],
            }
        ],
    }


def get_heatmap_option():
    """Heatmap chart configuration."""
    hours = [
        "12a",
        "1a",
        "2a",
        "3a",
        "4a",
        "5a",
        "6a",
        "7a",
        "8a",
        "9a",
        "10a",
        "11a",
        "12p",
        "1p",
        "2p",
        "3p",
        "4p",
        "5p",
        "6p",
        "7p",
        "8p",
        "9p",
        "10p",
        "11p",
    ]
    days = ["Sat", "Fri", "Thu", "Wed", "Tue", "Mon", "Sun"]

    # Generate random data for heatmap
    data = []
    for i in range(7):
        for j in range(24):
            data.append([j, i, random.randint(0, 10)])

    return {
        "title": {"text": "Weekly Activity Heatmap", "left": "center"},
        "tooltip": {"position": "top"},
        "grid": {"top": "15%", "bottom": "15%"},
        "xAxis": {"type": "category", "data": hours, "splitArea": {"show": True}},
        "yAxis": {"type": "category", "data": days, "splitArea": {"show": True}},
        "visualMap": {
            "min": 0,
            "max": 10,
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "0%",
        },
        "series": [
            {
                "type": "heatmap",
                "data": data,
                "label": {"show": False},
                "emphasis": {
                    "itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}
                },
            }
        ],
    }


def get_sankey_option():
    """Sankey chart configuration with energy flow data."""
    nodes = [
        {"name": "Agricultural 'waste'"},
        {"name": "Bio-conversion"},
        {"name": "Liquid"},
        {"name": "Losses"},
        {"name": "Solid"},
        {"name": "Gas"},
        {"name": "Biofuel imports"},
        {"name": "Biomass imports"},
        {"name": "Coal imports"},
        {"name": "Coal"},
        {"name": "Coal reserves"},
        {"name": "District heating"},
        {"name": "Industry"},
        {"name": "Heating and cooling - commercial"},
        {"name": "Heating and cooling - homes"},
        {"name": "Electricity grid"},
        {"name": "Over generation / exports"},
        {"name": "H2 conversion"},
        {"name": "Road transport"},
        {"name": "Agriculture"},
        {"name": "Rail transport"},
        {"name": "Lighting & appliances - commercial"},
        {"name": "Lighting & appliances - homes"},
        {"name": "Gas imports"},
        {"name": "Ngas"},
        {"name": "Gas reserves"},
        {"name": "Thermal generation"},
        {"name": "Geothermal"},
        {"name": "H2"},
        {"name": "Hydro"},
        {"name": "International shipping"},
        {"name": "Domestic aviation"},
        {"name": "International aviation"},
        {"name": "National navigation"},
        {"name": "Marine algae"},
        {"name": "Nuclear"},
        {"name": "Oil imports"},
        {"name": "Oil"},
        {"name": "Oil reserves"},
        {"name": "Other waste"},
        {"name": "Pumped heat"},
        {"name": "Solar PV"},
        {"name": "Solar Thermal"},
        {"name": "Solar"},
        {"name": "Tidal"},
        {"name": "UK land based bioenergy"},
        {"name": "Wave"},
        {"name": "Wind"},
    ]
    links = [
        {"source": "Agricultural 'waste'", "target": "Bio-conversion", "value": 124.729},
        {"source": "Bio-conversion", "target": "Liquid", "value": 0.597},
        {"source": "Bio-conversion", "target": "Losses", "value": 26.862},
        {"source": "Bio-conversion", "target": "Solid", "value": 280.322},
        {"source": "Bio-conversion", "target": "Gas", "value": 81.144},
        {"source": "Biofuel imports", "target": "Liquid", "value": 35},
        {"source": "Biomass imports", "target": "Solid", "value": 35},
        {"source": "Coal imports", "target": "Coal", "value": 11.606},
        {"source": "Coal reserves", "target": "Coal", "value": 63.965},
        {"source": "Coal", "target": "Solid", "value": 75.571},
        {"source": "District heating", "target": "Industry", "value": 10.639},
        {"source": "District heating", "target": "Heating and cooling - commercial", "value": 22.505},
        {"source": "District heating", "target": "Heating and cooling - homes", "value": 46.184},
        {"source": "Electricity grid", "target": "Over generation / exports", "value": 104.453},
        {"source": "Electricity grid", "target": "Heating and cooling - homes", "value": 113.726},
        {"source": "Electricity grid", "target": "H2 conversion", "value": 27.14},
        {"source": "Electricity grid", "target": "Industry", "value": 342.165},
        {"source": "Electricity grid", "target": "Road transport", "value": 37.797},
        {"source": "Electricity grid", "target": "Agriculture", "value": 4.412},
        {"source": "Electricity grid", "target": "Heating and cooling - commercial", "value": 40.858},
        {"source": "Electricity grid", "target": "Losses", "value": 56.691},
        {"source": "Electricity grid", "target": "Rail transport", "value": 7.863},
        {"source": "Electricity grid", "target": "Lighting & appliances - commercial", "value": 90.008},
        {"source": "Electricity grid", "target": "Lighting & appliances - homes", "value": 93.494},
        {"source": "Gas imports", "target": "Ngas", "value": 40.719},
        {"source": "Gas reserves", "target": "Ngas", "value": 82.233},
        {"source": "Gas", "target": "Heating and cooling - commercial", "value": 0.129},
        {"source": "Gas", "target": "Losses", "value": 1.401},
        {"source": "Gas", "target": "Thermal generation", "value": 151.891},
        {"source": "Gas", "target": "Agriculture", "value": 2.096},
        {"source": "Gas", "target": "Industry", "value": 48.58},
        {"source": "Geothermal", "target": "Electricity grid", "value": 7.013},
        {"source": "H2 conversion", "target": "H2", "value": 20.897},
        {"source": "H2 conversion", "target": "Losses", "value": 6.242},
        {"source": "H2", "target": "Road transport", "value": 20.897},
        {"source": "Hydro", "target": "Electricity grid", "value": 6.995},
        {"source": "Liquid", "target": "Industry", "value": 121.066},
        {"source": "Liquid", "target": "International shipping", "value": 128.69},
        {"source": "Liquid", "target": "Road transport", "value": 135.835},
        {"source": "Liquid", "target": "Domestic aviation", "value": 14.458},
        {"source": "Liquid", "target": "International aviation", "value": 206.267},
        {"source": "Liquid", "target": "Agriculture", "value": 3.64},
        {"source": "Liquid", "target": "National navigation", "value": 33.218},
        {"source": "Liquid", "target": "Rail transport", "value": 4.413},
        {"source": "Marine algae", "target": "Bio-conversion", "value": 4.375},
        {"source": "Ngas", "target": "Gas", "value": 122.952},
        {"source": "Nuclear", "target": "Thermal generation", "value": 839.978},
        {"source": "Oil imports", "target": "Oil", "value": 504.287},
        {"source": "Oil reserves", "target": "Oil", "value": 107.703},
        {"source": "Oil", "target": "Liquid", "value": 611.99},
        {"source": "Other waste", "target": "Solid", "value": 56.587},
        {"source": "Other waste", "target": "Bio-conversion", "value": 77.81},
        {"source": "Pumped heat", "target": "Heating and cooling - homes", "value": 193.026},
        {"source": "Pumped heat", "target": "Heating and cooling - commercial", "value": 70.672},
        {"source": "Solar PV", "target": "Electricity grid", "value": 59.901},
        {"source": "Solar Thermal", "target": "Heating and cooling - homes", "value": 19.263},
        {"source": "Solar", "target": "Solar Thermal", "value": 19.263},
        {"source": "Solar", "target": "Solar PV", "value": 59.901},
        {"source": "Solid", "target": "Agriculture", "value": 0.882},
        {"source": "Solid", "target": "Thermal generation", "value": 400.12},
        {"source": "Solid", "target": "Industry", "value": 46.477},
        {"source": "Thermal generation", "target": "Electricity grid", "value": 525.531},
        {"source": "Thermal generation", "target": "Losses", "value": 787.129},
        {"source": "Thermal generation", "target": "District heating", "value": 79.329},
        {"source": "Tidal", "target": "Electricity grid", "value": 9.452},
        {"source": "UK land based bioenergy", "target": "Bio-conversion", "value": 182.01},
        {"source": "Wave", "target": "Electricity grid", "value": 19.013},
        {"source": "Wind", "target": "Electricity grid", "value": 289.366},
    ]
    return {
        "title": {"text": "Node Align Right"},
        "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        "animation": False,
        "series": [
            {
                "type": "sankey",
                "emphasis": {"focus": "adjacency"},
                "nodeAlign": "right",
                "data": nodes,
                "links": links,
                "lineStyle": {"color": "source", "curveness": 0.5},
            }
        ],
    }


def get_nightingale_option():
    """Nightingale rose chart configuration."""
    return {
        "legend": {"top": "bottom"},
        "toolbox": {
            "show": True,
            "feature": {
                "mark": {"show": True},
                "dataView": {"show": True, "readOnly": False},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
            },
        },
        "series": [
            {
                "name": "Nightingale Chart",
                "type": "pie",
                "radius": [50, 250],
                "center": ["50%", "50%"],
                "roseType": "area",
                "itemStyle": {"borderRadius": 8},
                "data": [
                    {"value": 40, "name": "rose 1"},
                    {"value": 38, "name": "rose 2"},
                    {"value": 32, "name": "rose 3"},
                    {"value": 30, "name": "rose 4"},
                    {"value": 28, "name": "rose 5"},
                    {"value": 26, "name": "rose 6"},
                    {"value": 22, "name": "rose 7"},
                    {"value": 18, "name": "rose 8"},
                ],
            }
        ],
    }


def get_chord_option():
    """Chord diagram configuration with 10+ nodes."""
    return {
        "tooltip": {},
        "legend": {},
        "series": [
            {
                "type": "chord",
                "clockwise": False,
                "label": {"show": True},
                "lineStyle": {"color": "target"},
                "data": [
                    {"name": "A"},
                    {"name": "B"},
                    {"name": "C"},
                    {"name": "D"},
                    {"name": "E"},
                    {"name": "F"},
                    {"name": "G"},
                    {"name": "H"},
                    {"name": "I"},
                    {"name": "J"},
                    {"name": "K"},
                    {"name": "L"},
                ],
                "links": [
                    {"source": "A", "target": "B", "value": 40},
                    {"source": "A", "target": "C", "value": 20},
                    {"source": "A", "target": "E", "value": 35},
                    {"source": "B", "target": "D", "value": 20},
                    {"source": "B", "target": "F", "value": 30},
                    {"source": "C", "target": "G", "value": 25},
                    {"source": "C", "target": "H", "value": 15},
                    {"source": "D", "target": "I", "value": 28},
                    {"source": "E", "target": "J", "value": 32},
                    {"source": "F", "target": "K", "value": 18},
                    {"source": "G", "target": "L", "value": 22},
                    {"source": "H", "target": "A", "value": 25},
                    {"source": "I", "target": "B", "value": 29},
                    {"source": "J", "target": "C", "value": 17},
                    {"source": "K", "target": "D", "value": 34},
                    {"source": "L", "target": "E", "value": 19},
                    {"source": "A", "target": "D", "value": 15},
                    {"source": "B", "target": "E", "value": 12},
                    {"source": "F", "target": "G", "value": 21},
                    {"source": "H", "target": "I", "value": 31},
                ],
            }
        ],
    }


# ============================================================================
# Page Definition
# ============================================================================


@ui.page("/")
def home(ctx: Context):
    """Home page with comprehensive ECharts examples."""

    return Container(
        class_name="max-w-7xl mx-auto py-8 px-4 space-y-6",
        children=[
            # Header
            Row(
                class_name="space-y-2 mb-8 justify-between",
                children=[
                    Column(
                        children=[
                            Text(
                                "ECharts Extension for Refast",
                                class_name="text-3xl font-bold",
                            ),
                            Text(
                                "Interactive charts with full event support, theming, and dynamic updates",
                                class_name="text-muted-foreground text-lg",
                            ),
                        ]
                    ),
                    ThemeSwitcher(on_change=ctx.callback(theme_switched)),
                ],
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
                                            Text(
                                                "Event Info:",
                                                class_name="text-sm font-medium",
                                            ),
                                            Text(
                                                "Click on any chart element...",
                                                id="event-info",
                                                class_name="text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                    Column(
                                        class_name="space-y-1",
                                        children=[
                                            Text(
                                                "Hover Info:",
                                                class_name="text-sm font-medium",
                                            ),
                                            Text(
                                                "Hover over chart elements...",
                                                id="hover-info",
                                                class_name="text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Row 1: Bar and Line Charts
            Row(
                gap=6,
                class_name="items-stretch mb-6",
                children=[
                    # Bar Chart
                    Card(
                        class_name="flex-1 h-full",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Bar Chart"),
                                                    CardDescription(
                                                        "Click bars to see data, use button to randomize"
                                                    ),
                                                ]
                                            ),
                                            Badge("Interactive", variant="secondary"),
                                        ],
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4 h-full flex flex-col",
                                children=[
                                    ECharts(
                                        id="bar-chart",
                                        option=get_bar_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        # on_click=ctx.js(handle_chart_click),
                                        on_dblclick=ctx.callback(handle_chart_dblclick),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                        class_name="flex-1",
                                    ),
                                    Button(
                                        "Randomize Data",
                                        on_click=ctx.callback(update_bar_chart_data),
                                        class_name="w-full",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Line Chart
                    Card(
                        class_name="flex-1 h-full",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Line Chart"),
                                                    CardDescription(
                                                        "Multi-series with smooth lines and area fill"
                                                    ),
                                                ]
                                            ),
                                            Badge("Multi-Series", variant="secondary"),
                                        ],
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4 h-full flex flex-col",
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
                                        class_name="flex-1",
                                    ),
                                    Button(
                                        "Update Data",
                                        on_click=ctx.callback(update_line_chart_data),
                                        class_name="w-full",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Row 2: Pie and Scatter Charts
            Row(
                gap=6,
                class_name="items-stretch mb-6",
                children=[
                    # Pie Chart
                    Card(
                        class_name="flex-1 h-full",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Pie/Donut Chart"),
                                                    CardDescription(
                                                        "Donut style with emphasis label"
                                                    ),
                                                ]
                                            ),
                                            Badge("Animated", variant="secondary"),
                                        ],
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4 h-full flex flex-col",
                                children=[
                                    ECharts(
                                        id="pie-chart",
                                        option=get_pie_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                        class_name="flex-1",
                                    ),
                                    Button(
                                        "Randomize Values",
                                        on_click=ctx.callback(update_pie_chart_data),
                                        class_name="w-full",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Scatter Chart
                    Card(
                        class_name="flex-1 h-full",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Scatter Plot"),
                                                    CardDescription(
                                                        "With loading state demo"
                                                    ),
                                                ]
                                            ),
                                            Badge("Loading Demo", variant="secondary"),
                                        ],
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4 h-full flex flex-col",
                                children=[
                                    ECharts(
                                        id="scatter-chart",
                                        option=get_scatter_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="300px",
                                        theme="light",
                                        auto_resize=True,
                                        class_name="flex-1",
                                    ),
                                    Button(
                                        "Show Loading (2s)",
                                        on_click=ctx.callback(toggle_loading),
                                        class_name="w-full",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Row 3: Radar and Gauge Charts
            Row(
                gap=6,
                class_name="items-stretch mb-6",
                children=[
                    # Radar Chart
                    Card(
                        class_name="flex-1 h-full",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Radar Chart"),
                                                    CardDescription(
                                                        "Performance comparison with clear/restore"
                                                    ),
                                                ]
                                            ),
                                            Badge("Clear/Restore", variant="secondary"),
                                        ],
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="h-full flex flex-col min-h-0",
                                children=[
                                    ECharts(
                                        id="radar-chart",
                                        option=get_radar_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="310px",
                                        theme="light",
                                        auto_resize=True,
                                        class_name="flex-1 min-h-0",
                                    ),
                                    Row(
                                        gap=2,
                                        class_name="mt-auto",
                                        children=[
                                            Button(
                                                "Clear",
                                                on_click=ctx.callback(
                                                    clear_radar_chart
                                                ),
                                                variant="outline",
                                                class_name="flex-1",
                                            ),
                                            Button(
                                                "Restore",
                                                on_click=ctx.callback(
                                                    restore_radar_chart
                                                ),
                                                class_name="flex-1",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Gauge Chart
                    Card(
                        class_name="flex-1 h-full",
                        children=[
                            CardHeader(
                                children=[
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Column(
                                                children=[
                                                    CardTitle("Gauge Chart"),
                                                    CardDescription(
                                                        "System health indicator"
                                                    ),
                                                ]
                                            ),
                                            Badge("Progress", variant="secondary"),
                                        ],
                                    ),
                                ]
                            ),
                            CardContent(
                                class_name="h-full flex flex-col",
                                children=[
                                    ECharts(
                                        id="gauge-chart",
                                        option=get_gauge_option(),
                                        on_click=ctx.callback(handle_chart_click),
                                        height="350px",
                                        theme="light",
                                        auto_resize=True,
                                        class_name="flex-1",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Row 4: Heatmap (Full Width)
            Card(
                class_name="h-full mb-6",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Heatmap Chart"),
                                            CardDescription(
                                                "Weekly activity visualization with visual mapping"
                                            ),
                                        ]
                                    ),
                                    Badge("Full Width", variant="secondary"),
                                ],
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="h-full",
                        children=[
                            ECharts(
                                id="heatmap-chart",
                                option=get_heatmap_option(),
                                on_click=ctx.callback(handle_chart_click),
                                height="350px",
                                theme="light",
                                auto_resize=True,
                                class_name="flex-1",
                            ),
                        ],
                    ),
                ],
            ),
            # Row 5: Sankey Chart (Full Width)
            Card(
                class_name="h-full mb-6",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Sankey Chart"),
                                            CardDescription(
                                                "Energy flow with right-aligned nodes and adjacency emphasis"
                                            ),
                                        ]
                                    ),
                                    Badge("Flow", variant="secondary"),
                                ],
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="h-full",
                        children=[
                            ECharts(
                                id="sankey-chart",
                                option=get_sankey_option(),
                                on_click=ctx.callback(handle_chart_click),
                                height="600px",
                                theme="light",
                                auto_resize=True,
                                class_name="flex-1",
                            ),
                        ],
                    ),
                ],
            ),
            # Row 6: Nightingale Chart (Full Width)
            Card(
                class_name="h-full mb-6",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Nightingale Chart"),
                                            CardDescription(
                                                "Rose pie chart with toolbox and area-based petals"
                                            ),
                                        ]
                                    ),
                                    Badge("Rose Pie", variant="secondary"),
                                ],
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="h-full",
                        children=[
                            ECharts(
                                id="nightingale-chart",
                                option=get_nightingale_option(),
                                on_click=ctx.callback(handle_chart_click),
                                height="600px",
                                theme="light",
                                auto_resize=True,
                                class_name="flex-1",
                            ),
                        ],
                    ),
                ],
            ),
            # Row 7: Chord Chart (Full Width)
            Card(
                class_name="h-full mb-6",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Chord Diagram"),
                                            CardDescription(
                                                "Relationship visualization with 12 nodes and 20 connections"
                                            ),
                                        ]
                                    ),
                                    Badge("Relationships", variant="secondary"),
                                ],
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="h-full",
                        children=[
                            ECharts(
                                id="chord-chart",
                                option=get_chord_option(),
                                on_click=ctx.callback(handle_chart_click),
                                height="500px",
                                theme="light",
                                auto_resize=True,
                                class_name="flex-1",
                            ),
                        ],
                    ),
                ],
            ),
            # Dark Theme Example
            Card(
                class_name="bg-slate-900 h-full",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle(
                                                "Dark Theme Example",
                                                class_name="text-white",
                                            ),
                                            CardDescription(
                                                "Same bar chart with dark theme",
                                                class_name="text-slate-400",
                                            ),
                                        ]
                                    ),
                                    Badge(
                                        "theme='dark'",
                                        variant="outline",
                                        class_name="text-white border-slate-600",
                                    ),
                                ],
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="h-full",
                        children=[
                            ECharts(
                                id="dark-chart",
                                option=get_bar_option(),
                                on_click=ctx.callback(handle_chart_click),
                                height="300px",
                                theme="dark",
                                auto_resize=True,
                                class_name="flex-1",
                            ),
                        ],
                    ),
                ],
            ),
            # Footer
            Separator(),
            Column(
                class_name="text-center space-y-2 py-4",
                children=[
                    Text("ECharts Extension for Refast", class_name="font-medium"),
                    Text(
                        "Supports all ECharts chart types • Mouse events • Theming • Dynamic updates via setOption",
                        class_name="text-sm text-muted-foreground",
                    ),
                ],
            ),
        ],
    )


# Create FastAPI app
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
