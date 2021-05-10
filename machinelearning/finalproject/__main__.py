import pandas as pd
from machinelearning.finalproject import Diabetes

if __name__ == '__main__':
    csv_diabetes = 'data/machinelearning.finalproject/diabetes.csv'
    diabetes = Diabetes(csv_diabetes)

    csv_test_pos = 'data/machinelearning.finalproject/instances_positive.csv'
    group1 = pd.read_csv(csv_test_pos)

    csv_test_neg = 'data/machinelearning.finalproject/instances_negative.csv'
    group2 = pd.read_csv(csv_test_neg)

    print(diabetes.predict(group1))
    print(diabetes.predict(group2))
