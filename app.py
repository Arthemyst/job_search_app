import scraping_functions as sf
import pandas as pd

nofluffjobs_list = sf.nofluffjobs_page_job_offers()
df_raw_1 = pd.DataFrame.from_records(nofluffjobs_list)
df_1 = df_raw_1.copy()
df_1['publication_date'] = pd.to_datetime(df_1['publication_date'], infer_datetime_format=True)
df_1.drop_duplicates(subset=['publication_date', 'company', 'title'], inplace=True, ignore_index=True)
print(df_1)
print('*'*30)

bulldogjob_list = sf.bulldog_page_job_offers()
df_raw_2 = pd.DataFrame.from_records(bulldogjob_list)
df_2 = df_raw_2.copy()
df_2['publication_date'] = pd.to_datetime(df_2['publication_date'], infer_datetime_format=True)
df_2.drop_duplicates(subset=['publication_date', 'company', 'title'], inplace=True, ignore_index=True)
print(df_2)
print('*'*30)

print('After merging:')
df_3 = pd.concat([df_1, df_2], axis=0, ignore_index=True)
df_3.sort_values(['publication_date'], inplace=True, ascending=False)
print(df_3)
