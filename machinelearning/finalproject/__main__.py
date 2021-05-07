from machinelearning.finalproject import Diabetes, DiabetesData, PandasData

if __name__ == '__main__':
    df = DiabetesData('diabetes.csv').normalized(balance=True)
    print(type(PandasData(df)))
