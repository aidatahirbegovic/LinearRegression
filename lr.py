import os
import numpy as np
import pandas as pd

script_dir = os.getcwd()
file = 'dataLinearRegression2.csv'
data = pd.read_csv(os.path.normcase(os.path.join(script_dir, file)), sep=";") #.to_numpy()

#print(data.head(5))
data = data[["squareFootage", "constructionYear", "price"]] #changing and malipuating data squareFootage,roomNo,price

#print(data.head()) #printing 5

predict = "price" #label, what are u trying to get
X = np.array(data.drop([predict], 1))
y = np.array(data[predict])
#for i in range(5):
    #print('x =', X[i, ], ', y =', y[i])

m = 6479
f = 2
X_train = X[:m,:f]
#X_train = np.array(np.c_[np.ones(len(X_train),dtype='int64'),X_train])
y_train = np.array(y[:m])
X_test = X[m:,:f]
#X_test = np.array(np.c_[np.ones(len(X_test),dtype='int64'),X_test])
y_test = np.array(y[m:])

def feature_normalize(X):
  #Note here we need mean of indivdual column here, hence axis = 0
  mu = np.mean(X, axis = 0)  
  # Notice the parameter ddof (Delta Degrees of Freedom)  value is 1
  sigma = np.std(X, axis= 0, ddof = 1)  # Standard deviation (can also use range)
  X_norm = (X - mu)/sigma
  return X_norm, mu, sigma

def compute_cost(X, y, theta):
  predictions = X.dot(theta)
  #print('predictions= ', predictions[:5])
  errors = np.subtract(predictions, y)
  #print('errors= ', errors[:5]) 
  sqrErrors = np.square(errors)
  #print('sqrErrors= ', sqrErrors[:5]) 
  #J = 1 / (2 * m) * np.sum(sqrErrors)
  # OR
  # We can merge 'square' and 'sum' into one by taking the transpose of matrix 'errors' and taking dot product with itself
  # If your confuse about this try to do this with few values for better understanding  
  J = 1/(2 * m) * errors.T.dot(errors)

  return J

def gradient_descent(X, y, theta, alpha, iterations):
  cost_history = np.zeros(iterations)

  for i in range(iterations):
    predictions = X.dot(theta)
    #print('predictions= ', predictions[:5])
    errors = np.subtract(predictions, y)
    #print('errors= ', errors[:5])
    sum_delta = (alpha / m) * X.transpose().dot(errors);
    #print('sum_delta= ', sum_delta[:5])
    theta = theta - sum_delta;

    cost_history[i] = compute_cost(X, y, theta)  

  return theta, cost_history

X_train, mu, sigma = feature_normalize(X_train)

print('mu= ', mu)
print('sigma= ', sigma)
print('X_norm= ', X_train[:5])
n = len(y)
X_train = np.hstack((np.ones((m,1)), X_train))
X_train[:5]

theta = np.zeros(3)
iterations = 400;
alpha = 0.15;

# theta, cost_history = gradient_descent(X, y, theta, alpha, iterations)
# print('Final value of theta =', theta)
# print('First 5 values from cost_history =', cost_history[:5])
# print('Last 5 values from cost_history =', cost_history[-5 :])

import matplotlib.pyplot as plt
iterations = 400;
theta = np.zeros(3)

alpha = 0.005;
theta_1, cost_history_1 = gradient_descent(X_train, y_train, theta, alpha, iterations)

alpha = 0.01;
theta_2, cost_history_2 = gradient_descent(X_train, y_train, theta, alpha, iterations)

alpha = 0.02;
theta_3, cost_history_3 = gradient_descent(X_train, y_train, theta, alpha, iterations)

alpha = 0.03;
theta_4, cost_history_4 = gradient_descent(X_train, y_train, theta, alpha, iterations)

alpha = 0.15;
theta_5, cost_history_5 = gradient_descent(X_train, y_train, theta, alpha, iterations)

plt.plot(range(1, iterations +1), cost_history_1, color ='purple', label = 'alpha = 0.005')
plt.plot(range(1, iterations +1), cost_history_2, color ='red', label = 'alpha = 0.01')
plt.plot(range(1, iterations +1), cost_history_3, color ='green', label = 'alpha = 0.02')
plt.plot(range(1, iterations +1), cost_history_4, color ='yellow', label = 'alpha = 0.03')
plt.plot(range(1, iterations +1), cost_history_5, color ='blue', label = 'alpha = 0.15')

plt.rcParams["figure.figsize"] = (10,6)
plt.grid()
plt.xlabel("Number of iterations")
plt.ylabel("cost (J)")
plt.title("Effect of Learning Rate On Convergence of Gradient Descent")
plt.legend()

for i in range(len(X_test)):
      normalize_test_data = ((np.array([X_test[i][0], X_test[i][1]]) - mu) / sigma)
      normalize_test_data = np.hstack((np.ones(1), normalize_test_data))
      price = normalize_test_data.dot(theta_1)
      print('Predicted price of a ', X_test[i][0],  'sq-ft and ',  X_test[i][1], 'construction year house:', price, 'and real price is: ', y_test[i])
      price = normalize_test_data.dot(theta_2)
      print('Predicted price of a ', X_test[i][0],  'sq-ft and ',  X_test[i][1], 'construction year house:', price, 'and real price is: ', y_test[i])
      price = normalize_test_data.dot(theta_3)
      print('Predicted price of a ', X_test[i][0],  'sq-ft and ',  X_test[i][1], 'construction year house:', price, 'and real price is: ', y_test[i])
      price = normalize_test_data.dot(theta_4)
      print('Predicted price of a ', X_test[i][0],  'sq-ft and ',  X_test[i][1], 'construction year house:', price, 'and real price is: ', y_test[i])
      price = normalize_test_data.dot(theta_5)
      print('Predicted price of a ', X_test[i][0],  'sq-ft and ',  X_test[i][1], 'construction year house:', price, 'and real price is: ', y_test[i])

