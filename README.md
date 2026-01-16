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
from refast.components import Container, Button, Row
from refast_echarts import Echarts

# Extension is auto-discovered, no need to manually register
ui = RefastApp(title="Echarts Demo")


@ui.page("/")
def home(ctx: Context):
    return Container(
        children=[
            Echarts(
                id="my-component",
                value="Hello, World!",
            ),
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
| `value` | str | "" | The value to display |
| `on_change` | Callback | None | Called when the value changes |
| `id` | str | None | Component ID |
| `class_name` | str | "" | CSS classes to apply |

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
