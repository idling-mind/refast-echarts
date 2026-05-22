"""Tests for the ECharts component."""

import pytest
from refast_echarts import ECharts, Echarts, EchartsExtension


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

class TestImports:
    def test_echarts_importable(self):
        assert ECharts is not None

    def test_echarts_alias_same_class(self):
        """Echarts (old alias) should be the same class as ECharts."""
        assert Echarts is ECharts

    def test_extension_importable(self):
        assert EchartsExtension is not None


# ---------------------------------------------------------------------------
# Component instantiation & defaults
# ---------------------------------------------------------------------------

class TestEChartsDefaults:
    def setup_method(self):
        self.chart = ECharts()

    def test_component_type(self):
        assert self.chart.component_type == "ECharts"

    def test_default_option_is_empty_dict(self):
        assert self.chart.option == {}

    def test_default_theme_is_none(self):
        assert self.chart.theme is None

    def test_default_auto_resize_is_true(self):
        assert self.chart.auto_resize is True

    def test_default_loading_is_false(self):
        assert self.chart.loading is False

    def test_default_callbacks_are_none(self):
        for attr in (
            "on_click", "on_dblclick", "on_mousedown", "on_mousemove",
            "on_mouseup", "on_mouseover", "on_mouseout", "on_globalout",
            "on_contextmenu",
        ):
            assert getattr(self.chart, attr) is None

    def test_id_auto_generated(self):
        assert self.chart.id is not None
        assert isinstance(self.chart.id, str)
        assert len(self.chart.id) > 0

    def test_two_instances_have_different_ids(self):
        chart2 = ECharts()
        assert self.chart.id != chart2.id

    def test_default_width_height_none(self):
        assert self.chart.width is None
        assert self.chart.height is None


# ---------------------------------------------------------------------------
# Component instantiation with custom props
# ---------------------------------------------------------------------------

class TestEChartsCustomProps:
    def test_custom_id(self):
        chart = ECharts(id="my-chart")
        assert chart.id == "my-chart"

    def test_option_stored(self):
        option = {"series": [{"type": "bar", "data": [1, 2, 3]}]}
        chart = ECharts(option=option)
        assert chart.option == option

    def test_none_option_becomes_empty_dict(self):
        chart = ECharts(option=None)
        assert chart.option == {}

    def test_theme_string(self):
        chart = ECharts(theme="dark")
        assert chart.theme == "dark"

    def test_theme_dict(self):
        custom = {"color": ["#c23531"]}
        chart = ECharts(theme=custom)
        assert chart.theme == custom

    def test_auto_resize_false(self):
        chart = ECharts(auto_resize=False)
        assert chart.auto_resize is False

    def test_loading_true(self):
        chart = ECharts(loading=True)
        assert chart.loading is True

    def test_width_and_height(self):
        chart = ECharts(width="800px", height="500px")
        assert chart.width == "800px"
        assert chart.height == "500px"

    def test_class_name(self):
        chart = ECharts(class_name="my-class")
        assert chart.class_name == "my-class"

    def test_callback_stored(self):
        sentinel = object()
        chart = ECharts(on_click=sentinel)
        assert chart.on_click is sentinel


# ---------------------------------------------------------------------------
# render() output
# ---------------------------------------------------------------------------

class TestEChartsRender:
    def test_render_returns_dict(self):
        assert isinstance(ECharts().render(), dict)

    def test_render_type(self):
        rendered = ECharts().render()
        assert rendered["type"] == "ECharts"

    def test_render_id_present(self):
        chart = ECharts(id="test-id")
        assert chart.render()["id"] == "test-id"

    def test_render_has_props_and_children(self):
        rendered = ECharts().render()
        assert "props" in rendered
        assert "children" in rendered

    def test_render_option_in_props(self):
        option = {"xAxis": {"data": ["A", "B"]}}
        rendered = ECharts(option=option).render()
        assert rendered["props"]["option"] == option

    def test_render_default_style_is_none(self):
        """No width/height and no style dict → style should be None."""
        rendered = ECharts().render()
        assert rendered["props"]["style"] is None

    def test_render_height_applied_to_style(self):
        rendered = ECharts(height="400px").render()
        assert rendered["props"]["style"]["height"] == "400px"

    def test_render_width_applied_to_style(self):
        rendered = ECharts(width="100%").render()
        assert rendered["props"]["style"]["width"] == "100%"

    def test_render_width_and_height_merged(self):
        rendered = ECharts(width="600px", height="300px").render()
        style = rendered["props"]["style"]
        assert style["width"] == "600px"
        assert style["height"] == "300px"

    def test_render_explicit_style_merged_with_dimensions(self):
        rendered = ECharts(style={"border": "1px solid red"}, height="200px").render()
        style = rendered["props"]["style"]
        assert style["border"] == "1px solid red"
        assert style["height"] == "200px"

    def test_render_auto_resize_in_props(self):
        rendered = ECharts(auto_resize=False).render()
        assert rendered["props"]["auto_resize"] is False

    def test_render_loading_in_props(self):
        rendered = ECharts(loading=True).render()
        assert rendered["props"]["loading"] is True

    def test_render_theme_in_props(self):
        rendered = ECharts(theme="dark").render()
        assert rendered["props"]["theme"] == "dark"

    def test_render_callbacks_none_when_not_set(self):
        rendered = ECharts().render()
        props = rendered["props"]
        for key in ("on_click", "on_dblclick", "on_mouseover", "on_globalout"):
            assert props[key] is None

    def test_render_callback_serialized(self):
        """Callbacks with a serialize() method should be serialized."""

        class FakeCallback:
            def serialize(self):
                return {"event_id": "abc123"}

        cb = FakeCallback()
        rendered = ECharts(on_click=cb).render()
        assert rendered["props"]["on_click"] == {"event_id": "abc123"}

    def test_render_children_empty_by_default(self):
        assert ECharts().render()["children"] == []


# ---------------------------------------------------------------------------
# EchartsExtension
# ---------------------------------------------------------------------------

class TestEchartsExtension:
    def setup_method(self):
        self.ext = EchartsExtension()

    def test_name(self):
        assert self.ext.name == "refast-echarts"

    def test_version(self):
        assert self.ext.version == "0.1.0"

    def test_scripts_contains_js(self):
        assert any("refast-echarts.js" in s for s in self.ext.scripts)

    def test_static_path_exists(self):
        assert self.ext.static_path.exists()

    def test_static_js_file_exists(self):
        js_file = self.ext.static_path / "refast-echarts.js"
        assert js_file.exists(), f"Expected {js_file} to exist"

    def test_components_includes_echarts(self):
        assert ECharts in self.ext.components
