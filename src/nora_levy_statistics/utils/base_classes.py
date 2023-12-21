from nora_levy_statistics.utils import *
from helper_functions_ea import Logger

class BaseVariables:
    arguments = parsed_args
    environment = arguments.environment
    prefix = arguments.sj_prefix


class DataExtractor:
    logger = Logger("Nora Statistics Data").logger
    base_variables = BaseVariables()
    shooju_handler = SHOOJU_HANDLER
    selenium_handler = SELENIUM_HANDLER
    name = "Nora Levy Statistics"
    website_url = None
    metadata = None

    def extract(self):
        raise NotImplementedError

    def transform(self, data):
        raise NotImplementedError

    def load(self, df_final):
        self.logger.info("Uploading data for" + " " + self.name + " " + "to Shooju")
        self.shooju_handler.df_upload_long(
            job_name="nora_levy_statistics_etl",
            df=df_final,
            sid_prefix=self.base_variables.prefix,
        )
        self.logger.info("Data Uploaded successfully")

    def etl(self):
        try:
            data = self.extract()
        except Exception as err:
            raise RuntimeError(f"Scraper failed at extraction. Error was {err}") from err
        try:
            df_final = self.transform(data)
        except Exception as err:
            raise RuntimeError(f"Scraper failed at dataframe transformation. Error was {err}") from err
        try:
            self.load(df_final)
        except Exception as err:
            raise RuntimeError(f"Scraper failed at upload. Error was {err}") from err
