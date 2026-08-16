import matplotlib.pyplot as plt 
 
plt.figure(figsize=(10, 5.63)) 
plt.plot(weeks, revenue, color="#1F4E79", linewidth=2.5, label="Revenue") 
plt.grid(color="#DDDDDD", linewidth=0.5) 
plt.xlabel("Week", fontsize=13) 
plt.ylabel("Revenue ($)", fontsize=13) 
plt.xticks(fontsize=11) 
plt.yticks(fontsize=11) 
 
# Annotate the spike week with a callout box positioned above 
# and to the left of the point, pointing back to it with an arrow 
spike_week = 7 
spike_index = weeks.index(spike_week) 
spike_value = revenue[spike_index] 
offset = (max(revenue) - min(revenue)) * 0.15 
 
plt.annotate( 
   f"Week {spike_week}: Black Friday promo", 
   xy=(spike_week, spike_value), 
   xytext=(spike_week - 3, spike_value + offset), 
   arrowprops=dict(arrowstyle="->", color="#1F4E79"), 
   fontsize=10 
) 
 
plt.legend(loc="lower right", frameon=False) 
plt.tight_layout() 
plt.savefig("revenue_trend.png", dpi=300) 
