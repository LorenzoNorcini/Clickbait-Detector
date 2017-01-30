from sklearn.model_selection import GridSearchCV
from sklearn import svm

def get_best_SVM_model(data, targets, folds,
                       C=[2**i for i in range(-10, 10)],
                       gamma=[2**i for i in range(-10, 10)],
                       kernel=('linear', 'rbf')):

    params_grid = [
      {'C': C,
       'gamma': gamma,
       'kernel': kernel,
       'probability': True}
    ]

    grid_search = GridSearchCV(svm.SVC(), params_grid, n_jobs=-1, cv=folds)
    grid_search.fit(data, targets)
    return grid_search.best_estimator_ , grid_search.best_params_