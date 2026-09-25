import plotly.express as px 
 
fig = px.line(df, x="week", y="revenue", hover_data={"week": True, "revenue": ":$,.0f"}) 
fig.update_traces(hovertemplate="Week %{x}<br>Revenue: %{y}") 
fig.write_html("weekly_report.html") 
