def plot_correlation_matrix(df): 
   plt.figure(figsize=(10, 8)) 
    
   # Isolate numeric columns explicitly 
   numeric_df = df.select_dtypes(include=[np.number]) 
   corr_matrix = numeric_df.corr(method='pearson') 
    
   # Build an aesthetic heatmap mask to hide redundant upper triangle info 
   mask = np.triu(np.ones_like(corr_matrix, dtype=bool)) 
    
   sns.heatmap( 
       corr_matrix, 
       mask=mask, 
       annot=True, 
       cmap='coolwarm', 
       fmt=".2f", 
       linewidths=0.5 
   ) 
    
   plt.title('Organizational Feature Correlation Topology') 
   plt.show() 
