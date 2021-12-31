# climbing-inference

A [website](https://rishabhsamb.github.io/climbing-inference) that predicts (conservatively) your best rock climbing grade given physical data from prior logbook data.

The model was trained using various (non-deep) ML regression models (linear, k-nearest neighbours, decision tree, random forest, support vector), as seen in `training`.

After training, random forests seemed to provide the lowest MSE over a test set. Notably, a considerably less computationally
expensive option in k-nearest neighbours was only about 5% worse after hyperparameter optimizations.

The data was taken from the [dcohen21's 8a.nu scraped logbook](https://www.kaggle.com/dcohen21/8anu-climbing-logbook).
