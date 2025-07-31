import panel as pn
import pandas as pd
import holoviews as hv
import hvplot.pandas  # noqa
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from typing import Dict, List, Tuple

hv.extension("bokeh")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_currency(value: float) -> str:
    """
    Format currency values with smart abbreviations for large numbers.
    
    Args:
        value: The numeric value to format
        
    Returns:
        Formatted currency string
    """
    if value >= 1000000:
        return f"${value/1000000:.1f}M"
    elif value >= 1000:
        return f"${value/1000:.1f}K"
    else:
        return f"${value:,.2f}"

def get_card_style() -> Dict[str, str]:
    """
    Get consistent card styling for all dashboard components.
    
    Returns:
        Dictionary of CSS styles for cards
    """
    return {
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "5px",
        "box-shadow": "2px 2px 5px #eee",
        "word-wrap": "break-word",
        "overflow": "hidden",
        "white-space": "normal"
    }

def get_blue_palette() -> List[str]:
    """
    Get the blue color palette for consistent chart theming.
    
    Returns:
        List of blue color hex codes
    """
    return [
        '#1f77b4',  # Standard blue
        '#aec7e8',  # Light blue
        '#0066cc',  # Medium blue
        '#4d94d9',  # Sky blue
        '#0052a3',  # Dark blue
        '#6bb8ff',  # Bright light blue
        '#003d7a',  # Navy blue
        '#8cc8ff',  # Very light blue
    ]

def get_colors_for_categories(num_categories: int) -> List[str]:
    """
    Get appropriate colors for the given number of categories.
    
    Args:
        num_categories: Number of categories to get colors for
        
    Returns:
        List of color hex codes
    """
    blue_palette = get_blue_palette()
    
    if num_categories > len(blue_palette):
        # Repeat the palette if needed
        extended_palette = blue_palette * (num_categories // len(blue_palette) + 1)
        return extended_palette[:num_categories]
    else:
        return blue_palette[:num_categories]

# ============================================================================
# INDIVIDUAL METRIC CARD FUNCTIONS
# ============================================================================

def create_total_spend_card(total_spend: float) -> pn.indicators.Number:
    """
    Create the Total Spend metric card.
    
    Args:
        total_spend: The total spending amount
        
    Returns:
        Panel Number indicator for total spend
    """
    total_spend_str = format_currency(total_spend) if total_spend >= 10000 else f"${total_spend:,.2f}"
    
    return pn.indicators.Number(
        name="Total Spend",
        value=total_spend,
        format=total_spend_str,
        styles=get_card_style(),
        sizing_mode="stretch_width"
    )

def create_avg_transaction_card(avg_transaction: float) -> pn.indicators.Number:
    """
    Create the Average Transaction metric card.
    
    Args:
        avg_transaction: The average transaction amount
        
    Returns:
        Panel Number indicator for average transaction
    """
    avg_transaction_str = f"${avg_transaction:,.2f}"
    
    return pn.indicators.Number(
        name="Average Transaction",
        value=avg_transaction,
        format=avg_transaction_str,
        styles=get_card_style(),
        sizing_mode="stretch_width"
    )

def create_top_categories_card(spending_by_category: Dict[str, float]) -> pn.indicators.Number:
    """
    Create the Top Categories metric card.
    
    Args:
        spending_by_category: Dictionary of category spending amounts
        
    Returns:
        Panel Number indicator for top categories
    """
    # Sort by value and take only top 3
    sorted_categories = sorted(spending_by_category.items(), key=lambda x: x[1], reverse=True)[:3]
    
    if sorted_categories:
        # Create HTML formatted display with smaller font
        top_category_amount = sorted_categories[0][1]
        categories_html = f'<div style="font-size: 23.5px; line-height: 1.3; margin-top: 10px;">'
        categories_html += f"{sorted_categories[0][0]}: ${sorted_categories[0][1]:,.2f}"
        if len(sorted_categories) > 1:
            categories_html += f"<br>{sorted_categories[1][0]}: ${sorted_categories[1][1]:,.2f}"
        if len(sorted_categories) > 2:
            categories_html += f"<br>{sorted_categories[2][0]}: ${sorted_categories[2][1]:,.2f}"
        categories_html += '</div>'
        categories_display = categories_html
    else:
        top_category_amount = 0
        categories_display = '<div style="font-size: 20px; margin-top: 10px;">No data</div>'
    
    return pn.indicators.Number(
        name="Top Categories",
        value=top_category_amount,
        format=categories_display,
        styles=get_card_style(),
        sizing_mode="stretch_width"
    )

# ============================================================================
# INDIVIDUAL CHART FUNCTIONS
# ============================================================================

def create_bar_chart(df: pd.DataFrame) -> object:
    """
    Create a bar chart showing spending by category.
    
    Args:
        df: DataFrame with transaction data
        
    Returns:
        HoloViews bar chart object
    """
    spend_by_category = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    # Create a proper DataFrame for better tooltip formatting
    category_df = spend_by_category.reset_index()
    category_df.columns = ['category', 'total_amount']
    
    return category_df.hvplot.bar(
        x='category',
        y='total_amount',
        title="Total Spend by Category",
        xlabel="Category",
        ylabel="Total Amount ($)",
        height=250,
        grid=True,
        responsive=True,
    ).opts(
        tools=['hover'], 
        margin=(5, 5, 5, 5),
        hooks=[lambda plot, element: setattr(plot.handles['hover'], 'tooltips', [('Category', '@category'), ('Amount', '$@total_amount{0,0.00}')])]
    )

def create_line_chart(df: pd.DataFrame) -> object:
    """
    Create a line chart showing spending over time.
    
    Args:
        df: DataFrame with transaction data
        
    Returns:
        HoloViews line chart object
    """
    spend_over_time = df.set_index('transaction_date').resample('D')['amount'].sum()
    return spend_over_time.hvplot.line(
        title="Spend Over Time",
        xlabel="Date",
        ylabel="Total Amount ($)",
        height=270,
        grid=True,
        responsive=True,
    ).opts(tools=['hover'], margin=(-20, 5, 10, 5))

def create_donut_chart(df: pd.DataFrame) -> object:
    """
    Create a donut chart showing spending proportion by category.
    
    Args:
        df: DataFrame with transaction data
        
    Returns:
        Bokeh figure object or Panel Alert if no data
    """
    spend_by_category = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    data = spend_by_category.reset_index(name='amount')

    # Guard against division by zero if total is 0
    if data['amount'].sum() == 0:
        return pn.pane.Alert("No spending data to display in pie chart.", alert_type='info')

    # Apply blue color palette
    num_categories = len(data)
    data['color'] = get_colors_for_categories(num_categories)

    # Calculate angles and percentages
    data['angle'] = data['amount']/data['amount'].sum() * 2*pi
    data['percentage'] = (data['amount']/data['amount'].sum() * 100).round(1)

    # Create the figure
    pie_chart = figure(
        height=300,
        width=420,
        title="Spending Proportion by Category", 
        toolbar_location=None,
        tools="hover", 
        tooltips="@category: @amount{($0,0.00)} (@percentage{0.0}%)", 
        x_range=(-1.0, 0.8),
        y_range=(-0.8, 0.8),
        sizing_mode="fixed",
        margin=(10, 20, 5, 30)
    )

    # Add the donut wedges
    pie_chart.annular_wedge(
        x=-0.34, y=0,
        outer_radius=0.35,
        start_angle=cumsum('angle', include_zero=True), 
        end_angle=cumsum('angle'),
        line_color="white", 
        fill_color='color', 
        legend_field='category', 
        source=data
    )
    
    # Style the chart
    pie_chart.axis.axis_label = None
    pie_chart.axis.visible = False
    pie_chart.grid.grid_line_color = None
    pie_chart.outline_line_color = None
    pie_chart.border_fill_color = None
    
    # Style the title
    pie_chart.title.standoff = 5
    pie_chart.title.offset = -5
    
    # Style the legend
    pie_chart.legend.location = "right"
    pie_chart.legend.click_policy = "hide"
    pie_chart.legend.label_text_font_size = "9pt"
    pie_chart.legend.glyph_width = 15
    pie_chart.legend.glyph_height = 15
    pie_chart.legend.label_standoff = 40
    pie_chart.legend.spacing = 4
    pie_chart.legend.margin = 10

    return pie_chart

# ============================================================================
# MAIN ORCHESTRATION FUNCTIONS
# ============================================================================

def create_metric_cards(metrics: dict) -> pn.Row:
    """
    Creates a row of styled metric cards (Number indicators).

    Args:
        metrics: A dictionary containing the metrics data from the API.

    Returns:
        A Panel Row containing the metric cards.
    """
    # Handle empty or None metrics
    if not metrics or not isinstance(metrics, dict):
        metrics = {}
    
    # Extract and validate metric values
    total_spend = metrics.get('total_spent', 0)
    avg_transaction = metrics.get('average_transaction', 0)
    top_categories = metrics.get('spending_by_category', {})
    
    # Ensure values are numeric
    try:
        total_spend = float(total_spend) if total_spend is not None else 0.0
    except (ValueError, TypeError):
        total_spend = 0.0
        
    try:
        avg_transaction = float(avg_transaction) if avg_transaction is not None else 0.0
    except (ValueError, TypeError):
        avg_transaction = 0.0

    # Create individual metric cards
    total_spend_card = create_total_spend_card(total_spend)
    avg_transaction_card = create_avg_transaction_card(avg_transaction)
    top_categories_card = create_top_categories_card(top_categories)

    # Arrange cards in a responsive row with proper spacing
    return pn.Row(
        total_spend_card,
        avg_transaction_card,
        top_categories_card,
        sizing_mode="stretch_width",
        margin=(10, 5)
    )

def create_charts_view(df: pd.DataFrame) -> pn.Column:
    """
    Creates a view containing several charts based on the transaction data.

    Args:
        df: A pandas DataFrame with transaction data. It must contain
            'transaction_date', 'amount', and 'category' columns.

    Returns:
        A Panel Column containing the charts.
    """
    if df.empty:
        return pn.pane.Alert("No transaction data available for the selected period.", alert_type="info")

    # Ensure date column is in datetime format
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Create individual charts
    bar_chart = create_bar_chart(df)
    line_chart = create_line_chart(df)
    donut_chart = create_donut_chart(df)

    # Arrange charts in a layout with proper spacing
    charts_layout = pn.Column(
        pn.Row(
            pn.pane.HoloViews(bar_chart, sizing_mode="stretch_width"),
            pn.Spacer(width=20),
            pn.pane.Bokeh(donut_chart),
            sizing_mode="stretch_width"
        ),
        pn.pane.HoloViews(line_chart, sizing_mode="stretch_width"),
        sizing_mode="stretch_width"
    )
    
    return charts_layout

def create_filter_widgets(df: pd.DataFrame) -> dict:
    """
    Creates a dictionary of filter widgets based on the transaction data.

    Args:
        df: A pandas DataFrame with transaction data.

    Returns:
        A dictionary containing the configured filter widgets.
    """
    if df.empty:
        return {}
        
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    # Date Range Slider
    start_date = df['transaction_date'].min()
    end_date = df['transaction_date'].max()
    
    date_range_slider = pn.widgets.DateRangeSlider(
        name='Date Range',
        start=start_date,
        end=end_date,
        value=(start_date, end_date)
    )

    # Category Multi-Select
    categories = sorted(df['category'].unique().tolist())
    category_selector = pn.widgets.MultiChoice(
        name='Categories',
        options=categories,
        value=categories  # Default to all selected
    )

    return {
        "date_range": date_range_slider,
        "categories": category_selector
    } 