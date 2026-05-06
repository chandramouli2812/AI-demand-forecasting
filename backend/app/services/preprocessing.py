import pandas as pd

def preprocess(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    # Aggregate daily demand
    df = df.groupby('Order Date')['Quantity'].sum().reset_index()

    df.rename(columns={
        'Order Date': 'ds',
        'Quantity': 'y'
    }, inplace=True)

    return df