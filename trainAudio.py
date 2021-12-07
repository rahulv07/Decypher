import numpy as np
import sklearn.svm

shortTermWindow = 0.050
shortTermStep = 0.050
eps = 0.00000001


def train_svm(features, c_param, kernel='linear'):
    feature_matrix, labels = features_to_matrix(features)
    svm = sklearn.svm.SVC(C=c_param, kernel=kernel, probability=True,
                          gamma='auto')
    svm.fit(feature_matrix, labels)

    return svm


def normalize_features(features):
    temp_feats = np.array([])

    for count, f in enumerate(features):
        if f.shape[0] > 0:
            if count == 0:
                temp_feats = f
            else:
                temp_feats = np.vstack((temp_feats, f))
            count += 1

    mean = np.mean(temp_feats, axis=0) + 1e-14
    std = np.std(temp_feats, axis=0) + 1e-14

    features_norm = []
    for f in features:
        ft = f.copy()
        for n_samples in range(f.shape[0]):
            ft[n_samples, :] = (ft[n_samples, :] - mean) / std
        features_norm.append(ft)
    return features_norm, mean, std


def features_to_matrix(features):
    labels = np.array([])
    feature_matrix = np.array([])
    for i, f in enumerate(features):
        if i == 0:
            feature_matrix = f
            labels = i * np.ones((len(f), 1))
        else:
            feature_matrix = np.vstack((feature_matrix, f))
            labels = np.append(labels, i * np.ones((len(f), 1)))

    return feature_matrix, labels
