
#ADD FUNCTIONS

def group_age_category(cat):
    """Groups 'agecat' into Young, Middle, Elder."""
    if cat == 1:
        return 'Young'
    elif cat == 6:
        return 'Elder'
    else:
        return 'Middle'

KEEP_BODIES = {'SEDAN', 'STNWG', 'SUV', 'TRUCK', 'UTE', 'HDTOP', 'PANVN', 'MIBUS', 'COUPE'}
def group_vehicle_body(body_style):
    if pd.isna(body_style):
        return 'OTHER'
    normalized_style = str(body_style).upper()
    return normalized_style if normalized_style in KEEP_BODIES else 'OTHER'


ENCODING_MAP = {
    'marital_status': {'M': 0, 'S': 1},
    'time_driven': {'12am - 6 am': 0,  '12pm - 6pm': 1,  '6am - 12pm': 2,  '6pm - 12am': 3},
    'area': {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5},
    'agecat_grouped': {'Elder': 0, 'Middle': 1, 'Young': 2},
    'gender': {'F': 0, 'M': 1},
    'veh_color': {'black': 0,  'blue': 1,  'brown': 2,  'gray': 3,  'green': 4,  'red': 5,  'silver': 6,  'white': 7,  'yellow': 8},
    'engine_type': {'dissel': 0, 'electric': 1, 'hybrid': 2, 'petrol': 3},
    'veh_body_grouped': {'COUPE': 0,  'OTHER': 1,  'SEDAN': 2,  'STNWG': 3,  'SUV': 4,  'TRUCK': 5,  'UTE': 6}
}


# add to predict function after loading in df
df['agecat_grouped'] = df['agecat'].apply(group_age_category)
df['veh_body_grouped'] = df['veh_body'].apply(group_vehicle_body)

for col, mapping in ENCODING_MAP.items():
    if col in df.columns:
        df[col] = df[col].map(mapping)
        df[col] = df[col].fillna(-1)
        df[col] = df[col].astype(int)
    else:
        print(f"[Warning] Mapped column '{col}' not in payload.")