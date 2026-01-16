/**
 * Refast ECharts Extension
 *
 * This extension provides the ECharts component for creating
 * interactive charts with Apache ECharts.
 *
 * The component is registered with RefastClient's component registry
 * when this script loads after refast-client.js.
 */

import { ECharts } from './ECharts';

// Type definition for RefastClient
interface RefastClient {
  componentRegistry: {
    register: (name: string, component: React.ComponentType<unknown>) => void;
    has: (name: string) => boolean;
  };
  React: typeof import('react');
  ReactDOM: typeof import('react-dom');
  version: string;
}

declare global {
  interface Window {
    RefastClient?: RefastClient;
  }
}

/**
 * Register the ECharts component with Refast.
 *
 * This function is called immediately when the script loads.
 * It checks for RefastClient and registers the component.
 */
function registerComponents(): void {
  if (!window.RefastClient) {
    console.error(
      '[refast-echarts] RefastClient not found. ' +
      'Make sure refast-client.js is loaded before this script.'
    );
    return;
  }

  const { componentRegistry } = window.RefastClient;

  // Check if already registered (avoid duplicate registration)
  if (componentRegistry.has('ECharts')) {
    console.warn('[refast-echarts] ECharts already registered, skipping.');
    return;
  }

  // Register the component
  componentRegistry.register('ECharts', ECharts as React.ComponentType<unknown>);
  console.log('[refast-echarts] Registered ECharts component');
}

// Register components immediately
registerComponents();

// Export for direct imports (if bundled differently)
export { ECharts };
