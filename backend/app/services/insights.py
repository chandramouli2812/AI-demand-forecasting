def generate_insights(df):
    if df.empty or 'y' not in df.columns:
        return {
            'max_demand': None,
            'min_demand': None,
            'average_demand': None,
            'median_demand': None,
            'total_demand': None,
            'demand_range': None,
            'volatility': None,
            'trend': 'flat',
            'percent_change': None,
        }

    y = df['y'].dropna().astype(float)
    if y.empty:
        return {
            'max_demand': None,
            'min_demand': None,
            'average_demand': None,
            'median_demand': None,
            'total_demand': None,
            'demand_range': None,
            'volatility': None,
            'trend': 'flat',
            'percent_change': None,
        }

    first = y.iloc[0]
    last = y.iloc[-1]
    percent_change = None
    if first != 0:
        percent_change = round(((last - first) / first) * 100, 2)

    trend = 'flat'
    if last > first:
        trend = 'increasing'
    elif last < first:
        trend = 'decreasing'

    insights = {
        'max_demand': float(y.max()),
        'min_demand': float(y.min()),
        'average_demand': float(y.mean()),
        'median_demand': float(y.median()),
        'total_demand': float(y.sum()),
        'demand_range': float(y.max() - y.min()),
        'volatility': float(y.pct_change().std()) if len(y) > 1 else 0.0,
        'trend': trend,
        'percent_change': percent_change,
    }

    return insights
