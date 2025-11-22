export function MetricCard(props: {
  title: string;
  value: string;
  change: string;
  subtitle: string;
  icon: string;
  changeType: 'positive' | 'negative' | 'neutral';
}): string {
  const iconMap: Record<string, string> = {
    efficiency: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="9" stroke="#005a9c" stroke-width="2"/>
      <path d="M12 6v6l4 2" stroke="#005a9c" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
    time: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="9" stroke="#17a2b8" stroke-width="2"/>
      <path d="M12 7v5h5" stroke="#17a2b8" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
    warning: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 2l9 18H3L12 2z" stroke="#ffc107" stroke-width="2" stroke-linejoin="round"/>
      <path d="M12 10v4M12 16v1" stroke="#ffc107" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
    prediction: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M20 16l-8-8-4 4-6-6" stroke="#28a745" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="20" cy="16" r="2" fill="#28a745"/>
    </svg>`
  };

  const changeClass = props.changeType === 'positive' ? 'positive' : props.changeType === 'negative' ? 'negative' : 'neutral';

  return `
    <div class="metric-card">
      <div class="metric-header">
        <div class="metric-title">${props.title}</div>
        <div class="metric-icon">${iconMap[props.icon]}</div>
      </div>
      <div class="metric-value">${props.value}</div>
      <div class="metric-footer">
        <span class="metric-change ${changeClass}">${props.change}</span>
        <span class="metric-subtitle">${props.subtitle}</span>
      </div>
    </div>
  `;
}
