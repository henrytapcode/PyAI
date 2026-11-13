# Compare three scikit-learn pipelines fairly on the iris dataset.
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42, stratify=iris.target
)

candidates = [
    ("LogisticRegression", LogisticRegression(max_iter=1000)),
    ("KNeighbors", KNeighborsClassifier(n_neighbors=5)),
    ("DecisionTree", DecisionTreeClassifier(max_depth=3, random_state=0)),
]

best_name = ""
best_test = -1.0
print(f"{'Model':<20} {'Train':>7} {'Test':>7}")
for name, estimator in candidates:
    pipe = make_pipeline(StandardScaler(), estimator)
    pipe.fit(X_train, y_train)
    tr_acc = round(pipe.score(X_train, y_train), 3)
    te_acc = round(pipe.score(X_test, y_test), 3)
    print(f"{name:<20} {tr_acc:>7.3f} {te_acc:>7.3f}")
    if te_acc > best_test:
        best_test = te_acc
        best_name = name

print(f"Best on test: {best_name} ({best_test:.3f})")
