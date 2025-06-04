# src/main/resources/scripts/tab_classifier.py

import sys
import pickle

model_path = "src/main/resources/models/fast_invoice_ninja_tab_classifier.pkl"

with open(model_path, "rb") as f:
    model = pickle.load(f)

transcript = sys.argv[1]
tab_class = model.predict([transcript])[0]
print(tab_class)
