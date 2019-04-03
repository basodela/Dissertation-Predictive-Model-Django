import pandas as pd

from sklearn import linear_model

columns = ['target',
           'Lifter',
           'Snatch Lift 1 ',
           'Total',
           'Front Squat',
           'Back Squat',
           'lifter_id',

           'AgeGroupNumeric',
           'BodyweightNumeric',
           'U15', 'U17', 'U20',
           'U23', '102', '102+',
           '105', '109', '109+',
           '44', '45', '48',
           '49', '50', '53',
           '55', '56', '58',
           '59', '61', '62',
           '63', '64', '67',
           '69', '71', '73',
           '75', '76', '77',
           '81', '81+', '85',
           '87', '87+', '89',
           '90', '94', '96',
           'M']


def create_data_frame():
    return pd.read_csv('Users/scripts/logreg_development_1.csv')


def create_logistic_regression_model(training_features, target_feature):
    model = linear_model.LogisticRegression(solver='lbfgs')
    return model.fit(training_features, target_feature)


def create_models():
    df = create_data_frame()

    training_columns = columns[1:]
    training_features = df[training_columns]
    target_feature = df[columns[0]]

    return {
        'logistic_regression': create_logistic_regression_model(training_features, target_feature)
    }