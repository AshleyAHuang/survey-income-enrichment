import pandas as pd

def add_median_income(metadata_csv, income_csv, output_csv):
    metadata = pd.read_csv(metadata_csv)
    income = pd.read_csv(income_csv)

    metadata['building_zip'] = metadata['building_zip'].astype(str).str.extract(r'(\d{5})')[0].str.zfill(5)
    income['ZIP_Name'] = income['ZIP_Name'].astype(str).str.extract(r'(\d{5})')[0].str.zfill(5)

    merged = metadata.merge(
    income[['ZIP_Name', 'Median_Income_All_Households']],
    left_on='building_zip',
    right_on='ZIP_Name',
    how='left'
    )

    merged = merged.drop(columns=['ZIP_Name'])
    merged = merged.rename(columns={'Median_Income_All_Households': 'median_income_all_households_zip'})

    merged.to_csv(output_csv, index=False)
    print(f"Saved merged file to {output_csv}")
    print(f"Matched {merged['median_income_all_households_zip'].notna().sum()} of {len(merged)} rows.")

if __name__ == "__main__":
    add_median_income("survey-metadata.csv", "median_income_by_zip.csv", "metadata_with_income.csv")
