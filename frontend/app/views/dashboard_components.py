import panel as pn
import pandas as pd
import holoviews as hv
import hvplot.pandas  # noqa
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

hv.extension("bokeh")

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
    
    total_spend = metrics.get('total_spent', 0)
    avg_transaction = metrics.get('average_transaction', 0)
    
    # Ensure values are numeric (convert to float if needed)
    try:
        total_spend = float(total_spend) if total_spend is not None else 0.0
    except (ValueError, TypeError):
        total_spend = 0.0
        
    try:
        avg_transaction = float(avg_transaction) if avg_transaction is not None else 0.0
    except (ValueError, TypeError):
        avg_transaction = 0.0
    
    # Function to format large numbers compactly
    def format_currency(value):
        if value >= 1000000:
            return f"${value/1000000:.1f}M"
        elif value >= 1000:
            return f"${value/1000:.1f}K"
        else:
            return f"${value:,.2f}"
    
    # Format the values for display - use compact format for large numbers
    total_spend_str = format_currency(total_spend) if total_spend >= 10000 else f"${total_spend:,.2f}"
    avg_transaction_str = f"${avg_transaction:,.2f}"

    # Define common styles for the number indicators
    card_style = {
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "5px",
        "box-shadow": "2px 2px 5px #eee",
        "word-wrap": "break-word",
        "overflow": "hidden",
        "white-space": "normal"
    }

    # Create the individual metric cards
    total_spend_card = pn.indicators.Number(
        name="Total Spend",
        value=total_spend,
        format=total_spend_str,
        styles=card_style,
        sizing_mode="stretch_width"
    )

    avg_transaction_card = pn.indicators.Number(
        name="Average Transaction",
        value=avg_transaction,
        format=avg_transaction_str,
        styles=card_style,
        sizing_mode="stretch_width"
    )
    
    # Display top 3 categories only
    top_categories = metrics.get('spending_by_category', {})
    # Sort by value and take only top 3
    sorted_categories = sorted(top_categories.items(), key=lambda x: x[1], reverse=True)[:3]
    top_categories_list = [f"{cat}: ${val:,.2f}" for cat, val in sorted_categories]
    
    # Create Top Categories card using the same Number indicator approach
    # Format as HTML string with smaller font size
    if sorted_categories:
        # Create a simple formatted string showing just the first category as main value
        top_category_amount = sorted_categories[0][1]
        # Create HTML formatted display with smaller font
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
    
    # Use a Number indicator but with custom format to show our categories
    top_categories_md = pn.indicators.Number(
        name="Top Categories",
        value=top_category_amount,
        format=categories_display,
        styles=card_style,
        sizing_mode="stretch_width"
    )

    # Arrange cards in a responsive row with proper spacing
    return pn.Row(
        total_spend_card,
        avg_transaction_card,
        top_categories_md,
        sizing_mode="stretch_width",
        margin=(10, 5)  # Add margin to prevent overflow
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

    # 1. Bar Chart: Spending by Category
    spend_by_category = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    # Create a proper DataFrame for better tooltip formatting
    category_df = spend_by_category.reset_index()
    category_df.columns = ['category', 'total_amount']
    
    bar_chart = category_df.hvplot.bar(
        x='category',
        y='total_amount',
        title="Total Spend by Category",
        xlabel="Category",
        ylabel="Total Amount ($)",
        height=250,  # Much more compact height
        grid=True,
        responsive=True,
    ).opts(
        tools=['hover'], 
        margin=(5, 5, 5, 5),
        hooks=[lambda plot, element: setattr(plot.handles['hover'], 'tooltips', [('Category', '@category'), ('Amount', '$@total_amount{0,0.00}')])]
    )

    # 2. Line Chart: Spending Over Time
    spend_over_time = df.set_index('transaction_date').resample('D')['amount'].sum()
    line_chart = spend_over_time.hvplot.line(
        title="Spend Over Time",
        xlabel="Date",
        ylabel="Total Amount ($)",
        height=270,  # Reduced from 350 to match other charts
        grid=True,
        responsive=True,
    ).opts(tools=['hover'], margin=(-20, 5, 10, 5))  # Negative top margin to pull it up
    
    # 3. Pie Chart: Rebuilding with raw Bokeh for maximum stability
    # Prepare data for Bokeh wedge plot
    data = spend_by_category.reset_index(name='amount')

    # Guard against division by zero if total is 0
    if data['amount'].sum() == 0:
        pie_chart = pn.pane.Alert("No spending data to display in pie chart.", alert_type='info')
    else:
        # Create a blue-themed color palette with different shades
        num_categories = len(data)
        blue_palette = [
            '#1f77b4',  # Standard blue
            '#aec7e8',  # Light blue
            '#0066cc',  # Medium blue
            '#4d94d9',  # Sky blue
            '#0052a3',  # Dark blue
            '#6bb8ff',  # Bright light blue
            '#003d7a',  # Navy blue
            '#8cc8ff',  # Very light blue
        ]
        
        # Extend palette if we have more categories
        if num_categories > len(blue_palette):
            # Repeat the palette if needed
            extended_palette = blue_palette * (num_categories // len(blue_palette) + 1)
            data['color'] = extended_palette[:num_categories]
        else:
            data['color'] = blue_palette[:num_categories]

        data['angle'] = data['amount']/data['amount'].sum() * 2*pi
        data['percentage'] = (data['amount']/data['amount'].sum() * 100).round(1)

        pie_chart = figure(
            height=300,  # Much more compact to match bar chart
            width=420,   # Even wider to accommodate legend spacing
            title="Spending Proportion by Category", 
            toolbar_location=None,
            tools="hover", 
            tooltips="@category: @amount{($0,0.00)} (@percentage{0.0}%)", 
            x_range=(-1.0, 0.8),  # Extend right boundary to show full legend
            y_range=(-0.8, 0.8),  # Slightly wider range to prevent clipping
            sizing_mode="fixed",  # Use fixed sizing instead of stretch
            margin=(10, 20, 5, 30)   # Reduce right margin since we extended x_range
        )

        pie_chart.annular_wedge(
            x=-0.34, y=0,  # Move pie chart further left to create more space for legend
            outer_radius=0.35,  # Outer radius
            #inner_radius=0.15,  # Inner radius to create donut hole
            start_angle=cumsum('angle', include_zero=True), 
            end_angle=cumsum('angle'),
            line_color="white", 
            fill_color='color', 
            legend_field='category', 
            source=data
        )
        


        pie_chart.axis.axis_label=None
        pie_chart.axis.visible=False
        pie_chart.grid.grid_line_color = None
        
        # Remove borders and reduce padding
        pie_chart.outline_line_color = None
        pie_chart.border_fill_color = None
        
        # Reduce gap between title and chart
        pie_chart.title.standoff = 5   # Reduce space between title and plot area
        pie_chart.title.offset = -5    # Move title closer to chart
        
        # Improve legend positioning and make it more compact
        pie_chart.legend.location = "right"
        pie_chart.legend.click_policy = "hide"  # Allow hiding categories by clicking
        pie_chart.legend.label_text_font_size = "9pt"
        pie_chart.legend.glyph_width = 15
        pie_chart.legend.glyph_height = 15
        pie_chart.legend.label_standoff = 40  # Much more space between legend and chart
        pie_chart.legend.spacing = 4
        pie_chart.legend.margin = 10 # Extra margin around legend

    # Arrange charts in a layout with better spacing
    charts_layout = pn.Column(
        pn.Row(
            pn.pane.HoloViews(bar_chart, sizing_mode="stretch_width"),
            pn.Spacer(width=20),  # Small spacer between charts
            pn.pane.Bokeh(pie_chart),  # Wrap pie chart to control its behavior
            sizing_mode="stretch_width"
        ),
        # Remove spacer entirely for maximum closeness
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