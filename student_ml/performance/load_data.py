import pandas as pd
from performance.models import StudentPerformance
import os
def run():
    csv_file = os.path.join(os.path.dirname(__file__), 'dataset.csv')
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        StudentPerformance.objects.create(
            hours_studied=row['Hours Studied'],
            previous_scores=row['Previous Scores'],
            extracurricular=row['Extracurricular Activities'] == 'Yes',
            sleep_hours=row['Sleep Hours'],
            sample_papers=row['Sample Question Papers Practiced'],
            performance_index=row['Performance Index'],
)