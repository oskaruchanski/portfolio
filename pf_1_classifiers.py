# supervised machine learning models for gender classification
from sklearn import tree
from sklearn import svm
from sklearn import neighbors
from sklearn.linear_model import perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# initial dataset - height, weight, shoe size and gender
X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],
     [190, 90, 47], [175, 64, 39], [177, 70, 40], [159, 55, 37], [171, 75, 42],
     [181, 85, 43]]
Y = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female',
     'female', 'male', 'male']

# dataset for prediction
real_X = [[190, 70, 43], [184, 84, 44], [198, 92, 48], [183, 83, 44],
          [166, 47, 36], [170, 60, 38], [172, 64, 39], [182, 80, 42],
          [180, 80, 43]]
real_Y = ['male', 'male', 'male', 'male', 'female', 'female',
          'female', 'male', 'male']

# classfiers with default hyperparameters
clf_tree = tree.DecisionTreeClassifier()
clf_svc = svm.SVC(gamma='auto')
clf_knn = neighbors.KNeighborsClassifier()
clf_per = perceptron.Perceptron()
clf_nb = GaussianNB()
clf_nn = MLPClassifier(max_iter=1000)
classifiers = [clf_tree, clf_svc, clf_knn, clf_per, clf_nb, clf_nn]

# training models
for classifier in classifiers:
    classifier = classifier.fit(X, Y)

# predict and compare results
preditions = [i for i in range(7)]
accuracy = [i for i in range(7)]

for i, classifier in enumerate(classifiers):
    preditions[i] = classifier.predict(real_X)
    accuracy[i] = accuracy_score(real_Y, preditions[i])
    print(str(classifier)[:str(classifier).find(
        '(')], 'accuracy: ', round(accuracy[i], 2))
