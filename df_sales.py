import pandas as pd
import numpy as np
data = {
    "store_name": ["North Flagship", "Westside Hub", "North Bay"],
    "region": ["North", "West", "North"],
    "total_revenue": [12450.80, 8920.50, 5100.00],
    "transaction_count": [150, 85, 8]
}

df_sales = pd.DataFrame(data)
df_sales["avg_order_value"] =( df_sales["total_revenue"] / df_sales["transaction_count"]).round(2)
df_sales["performance_tier"]=np.where(df_sales["total_revenue"]>=10000,"High Performance","Standard Performance")
audit_df=df_sales[df_sales["transaction_count"]<10]
print(df_sales)
print(audit_df)