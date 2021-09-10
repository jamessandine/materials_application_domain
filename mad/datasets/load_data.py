import pandas as pd
import pkg_resources
import os

data_path = pkg_resources.resource_filename('mad', 'datasets/data')


def load(df, target, drop_cols=None):
    '''
    Returns data for regression task
    '''

    path = os.path.join(data_path, df)

    if '.csv' == df[-4:]:
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path, engine='openpyxl')

    if drop_cols:
        df.drop(drop_cols, axis=1, inplace=True)

    # Prepare data
    X = df.drop(target, axis=1)
    X_names = X.columns.tolist()
    X = X.values
    y = df[target].values

    data = {}
    data['data'] = X
    data['target'] = y
    data['feature_names'] = X_names
    data['target_name'] = target
    data['data_filename'] = path
    data['frame'] = df

    return data


def friedman():
    '''
    Load the Friedman dataset.
    '''

    # Dataset information
    df = 'friedman_data.csv'
    target = 'y'

    return load(df, target)


def super_cond():
    '''
    Load the super conductor data set.
    '''

    # Dataset information
    df = 'Supercon_data_features_selected.xlsx'
    target = 'ln(Tc)'
    drop_cols = [
                 'name',
                 'group',
                 'Tc',
                 ]

    return load(df, target, drop_cols)


def diffusion():
    '''
    Load the diffusion data set.
    '''

    # Dataset information
    df = 'Diffusion_Data_haijinlogfeaturesnobarrier_alldata.xlsx'
    target = 'E_regression'
    drop_cols = [
                 'Material compositions 1',
                 'Material compositions 2',
                 'E_regression_shift',
                 ]

    return load(df, target, drop_cols)


def perovskite_stability():
    '''
    Load the perovskite stability dataset.
    '''

    df = 'Perovskite_stability_Wei_updated_forGlenn.xlsx'
    target = 'EnergyAboveHull'

    return load(df, target)


def electromigration():
    '''
    Load the electronmigration dataset.
    '''

    df = 'Dataset_electromigration.xlsx'
    target = 'Effective_charge_regression'

    return load(df, target)


def thermal_conductivity():
    '''
    Load the thermal conductivity dataset.
    '''

    df = 'citrine_thermal_conductivity_simplified.xlsx'
    target = 'log(k)'

    return load(df, target)


def dielectric_constant():
    '''
    Load the dielectric constant dataset.
    '''

    df = 'dielectric_constant_simplified.xlsx'
    target = 'log(poly_total)'

    return load(df, target)


def double_perovskites_gap():
    '''
    Load the double perovskie gap dataset.
    '''

    df = 'double_perovskites_gap.xlsx'
    target = 'gap gllbsc'

    return load(df, target)


def elastic_tensor():
    '''
    Load the elastic tensor dataset.
    '''

    df = 'elastic_tensor_2015_simplified.xlsx'
    target = 'log(K_VRH)'

    return load(df, target)


def heusler_magnetic():
    '''
    Load the heussler magnetic dataset.
    '''

    df = 'heusler_magnetic_simplified.xlsx'
    target = 'mu_b saturation'

    return load(df, target)

def piezoelectric_tensor():
    '''
    Load the piezoelectric tensor data.
    '''

    df = 'piezoelectric_tensor.xlsx'
    target = 'log(eij_max)'

    return load(df, target)


def steel_yield_strength():
    '''
    Load the steel yield strenght dataset.
    '''

    df = 'steel_strength_simplified.xlsx'
    target = 'yield strength'

    return load(df, target)


def test():
    '''
    Load the test dataset.
    '''

    # Dataset information
    df = 'test_data.csv'
    target = 'y'

    return load(df, target)
