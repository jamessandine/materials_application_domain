from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import Lasso
from sklearn import cluster

from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.feature_selection import RFE
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from mad.datasets import aggregate, statistics
from mad.plots import versus
from mad.plots import parity

from mad.datasets import load_data
from mad.ml import splitters, predict, feature_selectors

import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')


def main():
    '''
    Test ml workflow
    '''

    seed = 14987
    save = 'run'
    points = None
    sampling = None

    # Load data
    data = load_data.diffusion()
    grouping = data['class_name']
    df = data['frame']
    X = data['data']
    y = data['target']

    # ML setup
    scale = StandardScaler()
    outer_split = LeaveOneGroupOut()
    inner_split = LeaveOneGroupOut()
    selector = feature_selectors.no_selection()

    # Do LASSO
    model = BaggingRegressor(base_estimator=Lasso())
    grid = {}
    grid['model__base_estimator__alpha'] = np.logspace(-5, 5, 11)
    pipe = Pipeline(steps=[
                           ('scaler', scale),
                           ('select', selector),
                           ('model', model)
                           ])
    lasso = GridSearchCV(pipe, grid, cv=inner_split)

    # Random forest regression
    grid = {}
    model = RandomForestRegressor()
    grid['model__n_estimators'] = [100]
    grid['model__max_features'] = [None]
    grid['model__max_depth'] = [None]
    pipe = Pipeline(steps=[
                           ('scaler', scale),
                           ('select', selector),
                           ('model', model)
                           ])
    rf = GridSearchCV(pipe, grid, cv=inner_split)

    # Make pipeline
    pipes = [lasso, rf]

    # Evaluate
    new_save = os.path.join(save, 'leaveout')
    predict.run(X, y, outer_split, pipes, new_save, seed, groups=grouping)

    # ML setup
    scale = StandardScaler()
    outer_split = RepeatedKFold(5, 10)
    inner_split = RepeatedKFold(5, 2)
    selector = feature_selectors.no_selection()

    # Do LASSO
    model = BaggingRegressor(base_estimator=Lasso())
    grid = {}
    grid['model__base_estimator__alpha'] = np.logspace(-5, 5, 11)
    pipe = Pipeline(steps=[
                           ('scaler', scale),
                           ('select', selector),
                           ('model', model)
                           ])
    lasso = GridSearchCV(pipe, grid, cv=inner_split)

    # Random forest regression
    grid = {}
    model = RandomForestRegressor()
    grid['model__n_estimators'] = [100]
    grid['model__max_features'] = [None]
    grid['model__max_depth'] = [None]
    pipe = Pipeline(steps=[
                           ('scaler', scale),
                           ('select', selector),
                           ('model', model)
                           ])
    rf = GridSearchCV(pipe, grid, cv=inner_split)

    # Make pipeline
    pipes = [lasso, rf]

    # Evaluate
    new_save = os.path.join(save, 'repkfold')
    predict.run(X, y, outer_split, pipes, new_save, seed, groups=grouping)

    # Combine and analyize data together
    aggregate.folds(save)  # Combine split data from directory recursively
    statistics.folds(save)  # Gather statistics from data
    parity.make_plots(save)  # Make parity plots
    versus.make_plots(save, points, sampling)  # RMSE vs metrics


if __name__ == '__main__':
    main()
