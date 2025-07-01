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
    
    # Format the values for display
    total_spend_str = f"${total_spend:,.2f}"
    avg_transaction_str = f"${avg_transaction:,.2f}"

    # Define common styles for the number indicators
    card_style = {
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "5px",
        "box-shadow": "2px 2px 5px #eee",
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
    
    # Display top categories as a simple markdown pane for now
    top_categories = metrics.get('spending_by_category', {})
    top_categories_list = [f"- {cat}: ${val:,.2f}" for cat, val in top_categories.items()]
    top_categories_md = pn.pane.Markdown(
        "**Top Categories**\n" + "\n".join(top_categories_list),
        styles=card_style,
        sizing_mode="stretch_width"
    )

    # Arrange cards in a responsive row
    return pn.Row(
        total_spend_card,
        avg_transaction_card,
        top_categories_md,
        sizing_mode="stretch_width"
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
    bar_chart = spend_by_category.hvplot.bar(
        title="Total Spend by Category",
        xlabel="Category",
        ylabel="Total Amount ($)",
        height=250,  # Much more compact height
        
        grid=True,
        responsive=True,
    ).opts(tools=['hover'], margin=(5, 5, 5, 5))  # Reduced margins

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
        num_categories = len(data)
        if num_categories > len(Category20c):
            # Repeat the palette if there are more than 20 categories
            palette = Category20c[len(Category20c)] * (num_categories // len(Category20c) + 1)
            data['color'] = palette[:num_categories]
        elif num_categories >= 3:
            data['color'] = Category20c[num_categories]
        else:
            # Use a simple palette for 1 or 2 categories
            data['color'] = ['#2ca02c', '#d62728'][:num_categories]

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

        pie_chart.wedge(
            x=-0.34, y=0,  # Move pie chart further left to create more space for legend
            radius=0.35,  # Slightly smaller radius to ensure it fits within bounds
            start_angle=cumsum('angle', include_zero=True), 
            end_angle=cumsum('angle'),
            line_color="white", 
            fill_color='color', 
            legend_field='category', 
            source=data
        )
        
        # Calculate positions for percentage labels
        import numpy as np
        data['start_angle_val'] = np.cumsum([0] + data['angle'].tolist()[:-1])
        data['mid_angle'] = data['start_angle_val'] + data['angle']/2
        data['label_x'] = -0.35 + 0.18 * np.cos(data['mid_angle'])  # Adjust for moved pie chart
        data['label_y'] = 0.18 * np.sin(data['mid_angle'])
        data['label_text'] = [f"{p}%" for p in data['percentage']]  # Add as column
        
        # Add percentage labels inside wedges
        pie_chart.text(
            x='label_x', 
            y='label_y', 
            text='label_text',  # Reference the column name
            source=data,
            text_align="center", 
            text_baseline="middle",
            text_color="black",
            text_font_size="8pt",
            text_font_style="bold"
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