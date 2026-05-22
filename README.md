# refast-echarts

Refast extension for ECharts

A [Refast](https://github.com/idling-mind/refast) extension that provides the `Echarts` component.

## Installation

```bash
pip install refast-echarts
```

## Usage

### Option 1: Auto-Discovery (Recommended)

When you install the package, Refast will automatically discover and load the extension:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container
from refast_echarts import ECharts

ui = RefastApp(title="ECharts Demo")


@ui.page("/")
def home(ctx: Context):
    option = {
        "title": {"text": "Monthly Sales"},
        "tooltip": {},
        "xAxis": {
            "data": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        },
        "yAxis": {},
        "series": [
            {
                "name": "Sales",
                "type": "bar",
                "data": [120, 200, 150, 80, 70, 110],
            }
        ],
    }
    return Container(
        children=[
            ECharts(option=option, height="400px"),
        ]
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Option 2: Manual Registration

If you want to disable auto-discovery and register extensions manually:

```python
from refast import RefastApp
from refast_echarts import Echarts, EchartsExtension

ui = RefastApp(
    title="Echarts Demo",
    auto_discover_extensions=False,
    extensions=[EchartsExtension()],
)
```

## Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `option` | dict | `{}` | ECharts option configuration object |
| `theme` | str \| dict | `None` | Theme name (`"light"`, `"dark"`) or custom theme object |
| `height` | str | `None` | Chart height (e.g. `"400px"`) |
| `width` | str | `None` | Chart width (e.g. `"100%"`) |
| `auto_resize` | bool | `True` | Auto-resize chart when container size changes |
| `loading` | bool | `False` | Show loading animation |
| `on_click` | Callback | `None` | Fired when clicking on a chart element |
| `on_mouseover` | Callback | `None` | Fired when hovering over a chart element |
| `id` | str | `None` | Component ID (required for `setOption` calls) |
| `class_name` | str | `""` | CSS classes to apply to the container |

## Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### Building the Frontend

```bash
cd frontend
npm install
npm run build
```

This builds the UMD bundle to `src/refast_echarts/static/`.

### Installing Locally

```bash
# Install with automatic frontend build (via hatch hook)
pip install -e .

# Or build frontend first, then install
cd frontend && npm install && npm run build && cd ..
pip install -e .
```

### Running the Example

```bash
python usage.py
```

Then open http://localhost:8000 in your browser.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
