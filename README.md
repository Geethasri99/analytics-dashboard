# analytics-dashboard

Interactive retail analytics dashboard built with Streamlit and Plotly. Visualises 5,000+ synthetic orders with real-time sidebar filters.

## Features

- KPI cards: total revenue, orders, avg order value, unique customers
- - Monthly revenue trend (area chart)
  - - Revenue by category (horizontal bar)
    - - Region breakdown (donut chart)
      - - Customer segmentation: Bronze / Silver / Gold / Platinum tiers
        - - Raw data explorer with top 500 rows
          - - @st.cache_data for fast re-renders on filter changes
           
            - ## Quick Start
           
            - ```bash
              pip install -r requirements.txt
              streamlit run app.py
              ```

              Open http://localhost:8501 in your browser.

              ## Tech Stack

              - Streamlit — dashboard framework
              - - Plotly Express — interactive charts
                - - Pandas / NumPy — data processing
