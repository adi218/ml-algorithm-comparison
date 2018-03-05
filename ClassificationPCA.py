import numpy as np
import scipy.io as io
import cv2
import PCA
import NeuralNetwork
import SVM
import LogisticReg


data = io.loadmat("ExtYaleB10.mat")

train = data['train']
test = data['test']
train = np.ndarray.tolist(train)[0]
test = np.ndarray.tolist(test)[0]
train = np.array(train)
test = np.array(test)
y_train = np.zeros((500, 10))
y_test = np.zeros((140, 10))

k = 0
for i in range(10):
    for j in range(k, k + 50):
        y_train[j][i] = 1
    k += 50

k = 0
for i in range(10):
    for j in range(k, k + 14):
        y_test[j][i] = 1
    k += 14

x_train = []
for i in range(len(train)):
    train_temp = train[i].T
    for j in range(len(train_temp)):
        x_train.append(train_temp[j].T)
x_train = np.array(x_train)

x__train_vec = []
for i in range(len(x_train)):
    x_temp = cv2.resize(x_train[i], (20, 17), interpolation=cv2.INTER_AREA)
    # plt.imshow(x_temp)
    # plt.show()
    x__train_vec.append(x_temp.flatten())
x_train_vec = np.array(x__train_vec)
# x_train_vec = ((x_train_vec - 128.0)/128.0) - 1

x_test = []
k = 0
y_test_log_svm = np.zeros((140,1))
for i in range(len(test)):
    test_temp = test[i].T
    for j in range(len(test_temp)):
        y_test_log_svm[k][0] = i
        x_test.append(test_temp[j].T)
        k += 1
x_test = np.array(x_test)

x_test_vec = []
for i in range(len(x_test)):
    x_temp = cv2.resize(x_test[i], (20, 17), interpolation=cv2.INTER_AREA)
    x_test_vec.append(x_temp.flatten())
x_test_vec = np.array(x_test_vec)
# x_test_vec = ((x_test_vec - 128.0)/128.0) - 1
print(x_test_vec.shape)

test = PCA.PCA(d=340)
mean1, basis1, new_x_data_train = test.pca(x_train_vec.T)
mean2, basis2, new_x_data_test = test.pca(x_test_vec.T)

# print(new_x_data_train.shape)

test1 = NeuralNetwork.NeuralNet(100, 55, 10, actv='sigmoid')
test1.train(new_x_data_train, y_train, new_x_data_test, y_test)

lambda_set = [100, 0.01, 0.001, 10, 1, 0.1]
test1 = LogisticReg.MultiClassLog(20, 0.000005, lambda_set, 20000, 2)
param, x_test1 = test1.classification(new_x_data_train, new_x_data_test, y_test_log_svm)
test1.test(param, x_test1, y_test_log_svm)

test2 = SVM.MultiClassSVM(1000, 1, 0.001)
param = test2.classification(new_x_data_train, new_x_data_test, y_test_log_svm)
test2.test(param, new_x_data_test, y_test_log_svm)