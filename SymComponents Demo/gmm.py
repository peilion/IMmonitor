import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal


def loadData(fileName):
    data = np.loadtxt(fileName)
    return data


def scaleData(dataMat):
    max = dataMat[:, 0].max()
    min = dataMat[:, 0].min()
    dataMat[:, 0] = (dataMat[:, 0] - min) / (max - min)
    return dataMat


def initializePara():
    theta = np.array([0.3, 0.7])
    mu = np.array([[0.2], [0.4]])
    sigma = np.array([0.3, 0.5])
    print("mu:", mu, "sigma:", sigma, "theta:", theta, sep='\n')
    return theta, mu, sigma


def eStep(theta, mu, sigma, dataMat):
    w = np.mat(np.zeros((20, 2)))
    for j in range(2):
        temp = multivariate_normal(mu[j], sigma[j]).pdf(dataMat[:, 0]) * theta[j]
        w[:, j] = np.matrix(temp).transpose()
    for i in range(20):
        w[i, :] = w[i, :] / np.sum(w[i, :])
    return w


def mStep(data, w):
    sigma = np.zeros(2)
    for j in range(2):
        theta[j] = np.sum(w[:, j]) / 20
        mu[j] = w[:, j].transpose() * data[:, 0] / np.sum(w[:, j])
        for i in range(20):
            sigma[j] += w[i, j] * (data[i, 0] - mu[j]) * (data[i, 0] - mu[j]) / np.sum(w[:, j])
    return theta, mu, sigma


# load data
data = loadData('heights.txt')
dataMat = np.matrix(data, copy=True).transpose()
m, n = dataMat.shape
# rescale data
dataMat = scaleData(dataMat)
# initialize parameters
theta, mu, sigma = initializePara()
numIter = 40
# train parameters by E-step and M-stemp
for i in range(numIter):
    w = eStep(theta, mu, sigma, dataMat)
    theta, mu, sigma = mStep(dataMat, w)
# calculate final w by trained parameters
print("mu:", mu, "sigma:", sigma, "theta:", theta, sep='\n')
w = eStep(theta, mu, sigma, dataMat)
cluster = w.argmax(axis=1).flatten().tolist()[0]
# get data for female and male
female = np.array([data[i] for i in range(20) if cluster[i] == 0])
male = np.array([data[i] for i in range(20) if cluster[i] == 1])
# plot
plt.plot(female, [0] * len(female), 'rs', label="female")
plt.plot(male, [0] * len(male), 'bo', label="male")
plt.legend(loc="best")
plt.title('GMM Clustering Result')
plt.show()
