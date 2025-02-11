import json
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.etf_holdings import ETFHoldings
from utils.aggregate_holdings import ETFAggregation

DATA_FOLDER = "data/"

st.title("ETF Portfolio Aggregator")
st.write(
    "This app aggregates the holdings of different ETFs and shows the normalized portfolio proportions."
)

# GET DATA
# Load symbol data from JSON file
with open(DATA_FOLDER + "symbols.json", "r+") as sb:
    symbols = json.load(sb)
    sorted_symbols = dict(sorted(symbols.items()))

# Display multiselect dropdown for the user to pick ETFs
selected_symbols = st.multiselect(
    "Select the ETFs you want to include in the portfolio",
    options=list(sorted_symbols.keys()),
    default=None,  # Default is None
)

# Create a 1x2 layout for the buttons (aligned left and right)
col1, col2 = st.columns([1, 1])

# Process button (left-aligned)
with col1:
    process_button = st.button("Process ETFs", disabled=not selected_symbols)
    if process_button:
        if not selected_symbols:
            st.write("Please select at least one ETF to view its holdings.")
        else:
            # Process ETF holdings for selected symbols
            holdings_results = {}

            for symbol in selected_symbols:
                etf = ETFHoldings(symbols[symbol])
                holdings_data = etf.get_holdings()
                holdings_results[symbol] = holdings_data

            # Save the results to session_state to persist it across interactions
            st.session_state.holdings_results = holdings_results

            # Create a sorted list of processed ETF symbols
            sorted_symbols = sorted(holdings_results.keys())
            # Display the processed ETF symbols in a human-readable format
            st.success(f"Symbols processed: {', '.join(sorted_symbols)}")

            # Enable the Aggregate ETFs button
            st.session_state.processed = True  # Flag to enable next button

# Aggregate button (right-aligned)
with col2:
    aggregate_button = st.button(
        "Aggregate ETFs", disabled=not getattr(st.session_state, "processed", False)
    )
    if aggregate_button:
        if (
            "holdings_results" not in st.session_state
            or not st.session_state.holdings_results
        ):
            st.write(
                "Please process the ETFs first by clicking the 'Process Selected ETFs' button."
            )
        else:
            # Use the holdings results stored in session_state
            holdings_results = st.session_state.holdings_results
            aggregator = ETFAggregation(holdings_results)
            agg_result = aggregator.process()

            # Store aggregated result to session_state
            st.session_state.agg_result = agg_result

            st.success("Aggregation complete!")

            # Enable the Display Results button
            st.session_state.aggregated = True  # Flag to enable next button

# Full-width row for Display Results button
display_col = st.columns([1])  # Single column for full-width layout

with display_col[0]:
    display_button = st.button(
        "Display Results", disabled=not getattr(st.session_state, "aggregated", False)
    )
    if display_button:
        if "agg_result" not in st.session_state or not st.session_state.agg_result:
            st.write(
                "Please first aggregate the ETFs by clicking the 'Aggregate ETFs' button."
            )
        else:
            # Use the aggregated result stored in session_state
            agg_result = st.session_state.agg_result

            # Create a dataframe for easy manipulation
            aggregated_df = pd.DataFrame(
                agg_result.items(), columns=["Symbols", "Normalized Percent"]
            )
            aggregated_df = aggregated_df.sort_values(
                by="Normalized Percent", ascending=False
            )

            # Create the pie chart using Plotly Express
            fig = px.pie(
                aggregated_df,
                names="Symbols",
                values="Normalized Percent",
                hover_data=["Symbols", "Normalized Percent"],
                title=None,
                hole=0.3,  # Makes it a doughnut chart
                labels={
                    "Symbols": "ETF Symbols",
                    "Normalized Percent": "Normalized Percent (%)",
                },
            )

            # Customize the 3D-like effect by increasing the margin and adding some effects
            fig.update_traces(
                textinfo="percent", pull=[0.1] * len(aggregated_df)
            )

            # Increase chart size for better visibility
            fig.update_layout(
                height=400,  # Adjust the height to make the chart larger
                width=700,  # Adjust the width for better fit
            )

            # Display the pie chart in Streamlit
            st.write("### Portfolio Proportions")
            st.plotly_chart(fig)

            # Display the tabular data at the bottom
            st.write("### Aggregated Holdings")
            st.dataframe(
                aggregated_df,
                use_container_width=True,
                hide_index=True,
                height=None,
            )
