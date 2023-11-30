import time

import pandas as pd
import os
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from helper_functions_ea import Logger, Selenium
from nora_levy_statistics.utils.base_classes import DataExtractor


class nora_levy(DataExtractor):  # make sure you rename the class to your preference
    """Make sure you implement all the methods required for your ETL"""
    url = "https://www.nora.ie/volumes-of-oil-consumption"
    main_file = '//*[@id="comp-lecxtmxg"]/ul/li/p/span/a/span/span'

    def __init__(self):
        self.logger = Logger("Nora Levy ETL").logger

    def extract(self):
        self.logger.info("Extracting Data")
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'downloads')

        selenium_handler = Selenium(downloads_path=path, headless=True)
        selenium_handler.driver.get(self.url)

        WebDriverWait(selenium_handler.driver, 60).until(
            ec.presence_of_element_located((By.XPATH, self.main_file)))
        selenium_handler.driver.find_element(By.XPATH, self.main_file).click()
        time.sleep(5)

        excel_file = glob.glob(os.path.join(path, '*.xls*'))
        selenium_handler.driver.quit()
        print('Done with extraction processing Transformation')

        return excel_file

    def transform(self, data):
        self.logger.info("Transforming data")
        excel_file = data
        excel_file_path = excel_file[0]

        df_final = pd.DataFrame()
        xl = pd.ExcelFile(excel_file_path)
        sheet_names = xl.sheet_names
        n = 4
        for i in range(n, len(sheet_names)):
            print('Processing Sheet', sheet_names[i])
            df = pd.read_excel(excel_file_path, sheet_names[i])
            df['Unnamed: 1'] = df['Unnamed: 1'].str.strip()
            Month_Index_1 = df.index[df['Unnamed: 1'] == 'January']
            Month_Index_2 = df.index[df['Unnamed: 1'] == 'December']
            df_new = df.iloc[Month_Index_1[0]:Month_Index_2[0] + 1]
            new_names = ['year', 'month', 'gasoline', 'biofuel_in_gasoline', 'kerosene', 'gas_oil_1000ppm',
                         'gas_oil_10ppm', 'motor_diesel', 'biofuel_in_motor_diesel', 'fuel_oil', 'bio_lpg',
                         'other_biofuel', 'all_fuels']
            df_new = df_new.copy()
            df_new.rename(columns=dict(zip(df_new.columns, new_names)), inplace=True)
            year = df[df['Unnamed: 1'] == 'YEAR'].iloc[0]['Unnamed: 2']
            update_date = df[df['Unnamed: 1'] == 'Last Updated'].iloc[0]['Unnamed: 3']
            df_new.loc[:, 'year'] = year
            df_new.loc[:, 'Last_Update'] = update_date
            month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
                             'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
                             'November': 11, 'December': 12}
            df_new['month'] = df_new['month'].apply(lambda x: month_mapping[x])
            df_new['date'] = pd.to_datetime(df_new[['year', 'month']].copy().assign(DAY=1))
            df_final = pd.concat([df_final, df_new], ignore_index=True)

        columns = ['gasoline', 'biofuel_in_gasoline', 'kerosene', 'gas_oil_1000ppm', 'gas_oil_10ppm', 'motor_diesel',
                   'biofuel_in_motor_diesel', 'fuel_oil', 'bio_lpg', 'other_biofuel', 'all_fuels']
        for col in columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0)

        df_final = pd.melt(df_final, id_vars=['date'], value_vars=columns)
        df_final['series_id_name'] = df_final['variable']

        return df_final


def main():
    nora_levy().etl()


if __name__ == "__main__":  # pragma: no cover
    main()
