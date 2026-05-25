/**
 * ECharts component for Refast
 *
 * Wraps Apache ECharts with full support for:
 * - All chart types
 * - Mouse events (click, dblclick, mousedown, etc.)
 * - Theming
 * - Auto-resize
 * - Bound methods (setOption, resize, clear, etc.)
 */

import React, { useRef, useEffect, useState } from 'react';
import * as echarts from 'echarts';
import type { EChartsOption, ECharts as EChartsInstance } from 'echarts';
import { cn } from './utils';

// ECharts event params type
interface EChartsEventParams {
  componentType?: string;
  seriesType?: string;
  seriesIndex?: number;
  seriesName?: string;
  name?: string;
  dataIndex?: number;
  data?: unknown;
  dataType?: string;
  value?: unknown;
  color?: string;
  event?: MouseEvent;
}

// Event handler type - receives serialized event params
type EventHandler = (data: Record<string, unknown>) => void;
type ResizeParams = Parameters<EChartsInstance['resize']>[0];

function resolveTheme(
  theme: string | object | undefined
): string | object | undefined {
  if (theme == null) {
    const root = document.documentElement;
    // If data-theme is explicitly set, trust it over the media query
    if (root.dataset.theme) {
      return root.dataset.theme === 'dark' ? 'dark' : 'light';
    }
    if (root.classList.contains('dark')) return 'dark';
    if (root.classList.contains('light')) return 'light';

    const body = document.body;
    if (body?.dataset.theme) {
      return body.dataset.theme === 'dark' ? 'dark' : 'light';
    }
    if (body?.classList.contains('dark')) return 'dark';
    if (body?.classList.contains('light')) return 'light';

    return window.matchMedia?.('(prefers-color-scheme: dark)')?.matches ? 'dark' : 'light';
  }

  if (typeof theme === 'string' && theme.toLowerCase() === 'auto') {
    return resolveTheme(undefined);
  }

  return theme;
}

export interface EChartsProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  option?: EChartsOption;
  theme?: string | object;
  initOpts?: {
    devicePixelRatio?: number;
    renderer?: 'canvas' | 'svg';
    useDirtyRect?: boolean;
    width?: number | string;
    height?: number | string;
    locale?: string;
  };
  autoResize?: boolean;
  loading?: boolean;
  loadingOpts?: {
    text?: string;
    color?: string;
    textColor?: string;
    maskColor?: string;
    zlevel?: number;
    fontSize?: number;
    showSpinner?: boolean;
    spinnerRadius?: number;
    lineWidth?: number;
    fontWeight?: string | number;
    fontStyle?: string;
    fontFamily?: string;
  };
  
  // Event callbacks - these are handler functions created by ComponentRenderer
  onClick?: EventHandler;
  onDblclick?: EventHandler;
  onMousedown?: EventHandler;
  onMousemove?: EventHandler;
  onMouseup?: EventHandler;
  onMouseover?: EventHandler;
  onMouseout?: EventHandler;
  onGlobalout?: EventHandler;
  onContextmenu?: EventHandler;
  
  // Refast internal
  'data-refast-id'?: string;
}

// Serialize ECharts event params to plain object
function serializeEventParams(params: EChartsEventParams): Record<string, unknown> {
  return {
    componentType: params.componentType,
    seriesType: params.seriesType,
    seriesIndex: params.seriesIndex,
    seriesName: params.seriesName,
    name: params.name,
    dataIndex: params.dataIndex,
    data: params.data,
    dataType: params.dataType,
    value: params.value,
    color: params.color,
  };
}

export const ECharts: React.FC<EChartsProps> = ({
  id,
  className,
  style,
  option,
  theme,
  initOpts,
  autoResize = true,
  loading = false,
  loadingOpts,
  onClick,
  onDblclick,
  onMousedown,
  onMousemove,
  onMouseup,
  onMouseover,
  onMouseout,
  onGlobalout,
  onContextmenu,
  'data-refast-id': dataRefastId,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<EChartsInstance | null>(null);
  const resizeObserverRef = useRef<ResizeObserver | null>(null);

  // Track resolved theme for auto-detection
  const isAutoTheme = theme == null || (typeof theme === 'string' && theme.toLowerCase() === 'auto');
  const [resolvedTheme, setResolvedTheme] = useState<string | object | undefined>(() => resolveTheme(theme));

  // Watch for system/DOM theme changes when in auto mode
  useEffect(() => {
    if (!isAutoTheme) {
      setResolvedTheme(theme);
      return;
    }

    const update = () => setResolvedTheme(resolveTheme(undefined));

    // Watch prefers-color-scheme
    const mq = window.matchMedia?.('(prefers-color-scheme: dark)');
    mq?.addEventListener('change', update);

    // Watch class/data-theme changes on <html> and <body>
    const observer = new MutationObserver(update);
    const observerOpts: MutationObserverInit = { attributeFilter: ['class', 'data-theme'], attributes: true };
    observer.observe(document.documentElement, observerOpts);
    if (document.body) observer.observe(document.body, observerOpts);

    return () => {
      mq?.removeEventListener('change', update);
      observer.disconnect();
    };
  }, [isAutoTheme, theme]);

  // Initialize chart
  useEffect(() => {
    if (!containerRef.current) return;

    // Dispose existing chart if any
    if (chartRef.current) {
      chartRef.current.dispose();
    }

    // Create chart instance
    const chart = echarts.init(containerRef.current, resolvedTheme, initOpts);
    chartRef.current = chart;

    // Set initial option
    if (option) {
      chart.setOption(option);
    }

    // Setup event handlers - callbacks are already handler functions from ComponentRenderer
    const events: Array<[string, EventHandler | undefined]> = [
      ['click', onClick],
      ['dblclick', onDblclick],
      ['mousedown', onMousedown],
      ['mousemove', onMousemove],
      ['mouseup', onMouseup],
      ['mouseover', onMouseover],
      ['mouseout', onMouseout],
      ['globalout', onGlobalout],
      ['contextmenu', onContextmenu],
    ];

    events.forEach(([eventName, handler]) => {
      if (handler) {
        chart.on(eventName, (params: unknown) => {
          // Call the handler with serialized event params
          handler(serializeEventParams(params as EChartsEventParams));
        });
      }
    });

    // Setup auto-resize
    if (autoResize) {
      resizeObserverRef.current = new ResizeObserver(() => {
        chart.resize();
      });
      resizeObserverRef.current.observe(containerRef.current);
    }

    // Cleanup
    return () => {
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
        resizeObserverRef.current = null;
      }
      if (chartRef.current) {
        chartRef.current.dispose();
        chartRef.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resolvedTheme]); // Re-init on theme change (includes auto-detected changes)

  // Update option when it changes
  useEffect(() => {
    if (chartRef.current && option) {
      chartRef.current.setOption(option, { notMerge: false, lazyUpdate: false });
    }
  }, [option]);

  // Handle loading state
  useEffect(() => {
    if (chartRef.current) {
      if (loading) {
        chartRef.current.showLoading('default', loadingOpts);
      } else {
        chartRef.current.hideLoading();
      }
    }
  }, [loading, loadingOpts]);

  // Attach bound methods to DOM element
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // setOption - update chart options
    (container as unknown as Record<string, unknown>).setOption = (
      newOption: EChartsOption,
      notMerge?: boolean,
      lazyUpdate?: boolean
    ) => {
      chartRef.current?.setOption(newOption, { notMerge, lazyUpdate });
    };

    // resize - resize the chart
    (container as unknown as Record<string, unknown>).resize = (opts?: ResizeParams) => {
      chartRef.current?.resize(opts);
    };

    // clear - clear the chart
    (container as unknown as Record<string, unknown>).clear = () => {
      chartRef.current?.clear();
    };

    // showLoading - show loading animation
    (container as unknown as Record<string, unknown>).showLoading = (
      type?: string,
      opts?: object
    ) => {
      chartRef.current?.showLoading(type || 'default', opts);
    };

    // hideLoading - hide loading animation
    (container as unknown as Record<string, unknown>).hideLoading = () => {
      chartRef.current?.hideLoading();
    };

    // getDataURL - get chart as data URL
    (container as unknown as Record<string, unknown>).getDataURL = (opts?: {
      type?: 'png' | 'jpeg' | 'svg';
      pixelRatio?: number;
      backgroundColor?: string;
      excludeComponents?: string[];
    }) => {
      return chartRef.current?.getDataURL(opts);
    };

    // dispose - dispose the chart instance
    (container as unknown as Record<string, unknown>).dispose = () => {
      if (chartRef.current) {
        chartRef.current.dispose();
        chartRef.current = null;
      }
    };

    // getOption - get current chart option
    (container as unknown as Record<string, unknown>).getOption = () => {
      return chartRef.current?.getOption();
    };

    // Cleanup bound methods
    return () => {
      if (container) {
        delete (container as unknown as Record<string, unknown>).setOption;
        delete (container as unknown as Record<string, unknown>).resize;
        delete (container as unknown as Record<string, unknown>).clear;
        delete (container as unknown as Record<string, unknown>).showLoading;
        delete (container as unknown as Record<string, unknown>).hideLoading;
        delete (container as unknown as Record<string, unknown>).getDataURL;
        delete (container as unknown as Record<string, unknown>).dispose;
        delete (container as unknown as Record<string, unknown>).getOption;
      }
    };
  }, []);

  // Default style for container
  const containerStyle: React.CSSProperties = {
    width: '100%',
    height: '400px',
    ...style,
  };

  return (
    <div
      ref={containerRef}
      id={id}
      className={cn('refast-echarts', className)}
      style={containerStyle}
      data-refast-id={dataRefastId}
    />
  );
};

ECharts.displayName = 'ECharts';
