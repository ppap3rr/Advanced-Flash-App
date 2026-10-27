### Advanced Flash App

A desktop mental arithmetic trainer primarily focusing on non addition-subtraction questions built with Python and CustomTkinter. The app provides timed arithmetic practice, records, performance, and explores basic machine learning to tailor questions to the user's accuracy and speed. 

### Features

 - Practice multiplication, division, squares, square roots, cube roots, and difference of squares in a timed setting. 
 - Configure practice settings
 - Review practice history and previous performance statistics 
 - Record answer correctness and response times 
 - Use ML model to estimate answer correctness using engineered features 

## Getting Started

- Python 3.11 (recommended for this project)
- Git (to clone the repository)

### Installation

```powershell
git clone https://github.com/YOUR_USERNAME/Advanced-Flash-App.git
cd Advanced-Flash-App
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Replace `YOUR_USERNAME` with your GitHub username. If you do not have `requirements.txt` yet, generate and review one from the environment that runs the project before publishing these instructions.

> **Note:** The app may require the saved model files (`model.pkl`, `scaler.pkl`, and `training_columns.pkl`) for its prediction features. Make sure they are available, or document how to generate them with `train_model.py`. Never load untrusted pickle files.

## Machine Learning

The project includes a logistic regression classifier trained on arithmetic-attempt data. Feature engineering is handled in `features.py`, training in `train_model.py`, and prediction in `predictor.py`.

The model uses features derived from arithmetic questions and recorded attempts, such as operand sizes and digit patterns. Depending on the saved model's feature set, it may also use response time. If response time is an input, predictions using it are **not** pre-question difficulty estimates: the response time must first be known.

The model is an experimental component of the app, not a guarantee of a particular user's future performance. Add evaluation results here once you've documented the training/test split and validation method.

## Future Improvements

- Adaptive question selection based on user performance
- More detailed progress visualizations
- Improved model evaluation and retraining workflows
- Optional user profiles and data synchronization

## Credits & Attribution

### Libraries

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — by Tom Schimansky; desktop interface (MIT license).
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) — by the scikit-learn contributors; machine learning (BSD-3-Clause license).

### Icons

- **Settings:** [Icons8](https://icons8.com/icons/set/settings-page--yellow)
- **Stop:** [IconsDB](https://www.iconsdb.com/red-icons/square-rounded-icon.html)
- **Start:** [IconsDB](https://www.iconsdb.com/green-icons/play-icon.html)
- **History:** [Icones.pro](https://icones.pro/en/history-history-icon-png-symbol-blue/)
- **Progress:** [Icons8](https://icons8.com/icon/nqb0Et2diOFc/tasks)

Third-party assets remain subject to their respective licenses. Verify the terms for each icon, especially the Icones.pro asset, and retain any required license notices when distributing the app. A README credit does not replace license compliance.

## License

No license has been selected for this project's original code yet. Add a `LICENSE` file if you decide to grant others permission to reuse it. Third-party components retain their own licenses.
