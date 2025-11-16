## Team Name: FutureBright Actuarial Intelligence (AI)

View completed FutureBright AI website here!
[FutureBright AI](https://auto-risk-ui-274054009647.us-central1.run.app)

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

#### 3. (Optional) Cloud Deployment
Prerequisites: You will need to have created a Google Cloud Platform account to access, deploy, and maintain live deployments of any applications.
- Login to Google Cloud via your terminal:
```
gcloud login
```
- Deploy the backend environment, containing the saved model, model features, and prediction API endpoint using Flask. First, enter the backend directory:
```
cd backend
```
- Build a temporary image of the environment with your unique project id, application name, and latest version number:
```
gcloud builds submit \ --tag gcr.io/'YOUR PROJECT ID'/auto-risk-api:'LATEST VERSION NUMBER'
```
- Deploy the image of the backend application to Cloud Run:
```
gcloud run deploy auto-risk-api \
  --image gcr.io/'YOUR PROJECT ID'/auto-risk-api:'LATEST VERSION NUMBER' \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated # DISCLAIMER : allows any entity to call this api! do not include any sensitive information in your application if using this
```
- Deploy the frontend website, containing the source code and styling. First, enter the frontend directory:
```
cd ..
cd frontend
```
- Build a temporary image of the environment with your unique project id, application name, and latest version number:
```
gcloud builds submit \ --tag gcr.io/'YOUR PROJECT ID'/auto-risk-ui:'LATEST VERSION NUMBER'
```
- Deploy the image of the frontend application to Cloud Run:
```
gcloud run deploy auto-risk-ui \
  --image gcr.io/'YOUR PROJECT ID'/auto-risk-ui:'LATEST VERSION NUMBER' \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated # DISCLAIMER : allows any entity to visit this website! do not include any sensitive information in your application if using this
```

### Instructions for Use
To reproduce the results, begin in the `backend` folder and run the entirety of the the following notebooks in the order identified below:
* `data_collection.ipynb`
* `data_exploration.ipynb`
* `model_implementation.ipynb`

Visit the live [FutureBright AI](https://auto-risk-ui-274054009647.us-central1.run.app) website to test real-time calculation of expected loss and risk segmentation.

### Disclaimers
#### 1. Data Source
This model is trained exclusively on the `synthetic_auto_policies_model_data_10042025.csv` dataset. This data is synthetic and for demonstration purposes only. The model, its predictions, and any insights do not reflect real-world financial data and should not be used for actual underwriting or financial decisions.

#### 2. Model & Encoding
The model's performance is entirely dependent on the feature engineering and `encoding_map` generated in the `data_exploration.ipynb` notebook, and also defined as `ENCODING_MAP` in the `app.py` file. The API endpoint requires this exact mapping to function. Any change to the encoding logic or the model training will _require_ the API's `ENCODING_MAP` constant to be updated.

#### 3. Ethical & Regulatory Considerations
This model uses several variables (e.g., `credit_score`, `area`, `gender`) that may be considered "proxy variables" for protected classes. In a real-world scenario, the use of such data is heavily regulated and may be subject to legal and ethical review to ensure fairness and prevent disparate impact. This model is a technical prototype and has not undergone such a review.






