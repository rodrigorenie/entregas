from machinelearning.finalproject import Diabetes, DiabetesData, RocketFrame

if __name__ == '__main__':
    df = DiabetesData('diabetes.csv').data
    #print(RocketFrame(df, ['class']).categoricals)
    df.rocket.classnames = ['class']
    print(df.rocket.normalized.balanced)
