## Team Name: FutureBright Actuarial Intelligence (AI)

Team Members: 

Ashwin Dervesh, Varun Vaidya, Lauren Tetzlaff, Aliese Schmaltz

### Context
FutureBright Insurance’s automobile division wants to improve its ability to assess customer risk. Currently, underwriting decisions might rely on broad rating tables and limited historical averages. By building a risk segmentation model, our team aims to use data-driven insights to:
- Quantify each policyholder’s expected loss (claim cost per exposure).
- Classify potential customers into Low, Medium, and High risk segments.
- Enable more accurate pricing, targeted underwriting, and strategic marketing.
### Goal: Segment Risk Profiles
Approach:
- Develop an XGBoost-based predictive model that estimates each customer’s expected loss and assigns them to a risk category (Low/Medium/High)
- Visualize risk distribution by features like vehicle age, driver age, region, or policy type.
- Deploy to cloud and website - business members select new customer information, and our feature returns the customer's risk level

### Value:
- Enables differentiated pricing or eligibility thresholds, and potentially more profitable business outcomes.

## Development Notes

### Project Setup
This project uses a specific set of Python libraries and relies on a data pipeline where analysis (in a notebook) creates assets used by the model (in the API).

#### 1. Environment Setup
It is highly recommended to use a virtual environment (like venv or conda) to manage dependencies.
```
# Create a virtual environment
python -m venv .venv
```
Activate it:
```
# On Windows:
.\.venv\Scripts\activate
```
```
# On macOS/Linux:
source .venv/bin/activate
```
#### 2. Install Dependencies
Run the following command inside of your virtual environment:
```
pip install -r backend/requirements.txt
```

### Instructions for Use
To reproduce the results, begin in the `backend` folder and run the entirety of the the following notebooks in the order identified below:
* `data_collection.ipynb`
* `data_exploration.ipynb`
* `model_implementation.ipynb`

ADD WEBSITE INSTRUCTIONS HERE

### Disclaimers
#### 1. Data Source
This model is trained exclusively on the `synthetic_auto_policies_model_data_10042025.csv` dataset. This data is synthetic and for demonstration purposes only. The model, its predictions, and any insights do not reflect real-world financial data and should not be used for actual underwriting or financial decisions.

#### 2. Model & Encoding
The model's performance is entirely dependent on the feature engineering and `encoding_map` generated in the `data_exploration.ipynb` notebook and also defined as `ENCODING_MAP` in the `app.py` file. The API endpoint requires this exact mapping to function. Any change to the encoding logic or the model training will _require_ the API's `ENCODING_MAP` constant to be updated.

#### 3. Ethical & Regulatory Considerations
This model uses several variables (e.g., `credit_score`, `area`, `gender`) that may be considered "proxy variables" for protected classes. In a real-world scenario, the use of such data is heavily regulated and may be subject to legal and ethical review to ensure fairness and prevent disparate impact. This model is a technical prototype and has not undergone such a review.



