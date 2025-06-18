from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_ml_model(df):
    df = df.dropna().copy()
    df['Future_Close'] = df['Close'].shift(-10)
    df['Target'] = (df['Future_Close'] > df['Close']).astype(int)

    features = ['MA20', 'MA50', 'RSI', 'BB_upper', 'BB_lower']
    X = df[features]
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    return model, acc
