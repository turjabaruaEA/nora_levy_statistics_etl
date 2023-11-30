import argparse
from datetime import datetime
from helper_functions_ea import Selenium, ShoojuTools, check_env

check_env()

# Initiate all your handlers here

SELENIUM_HANDLER = Selenium(headless=True)
SHOOJU_HANDLER = ShoojuTools()
SHOOJU_ENGINE = SHOOJU_HANDLER.sj


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parameters for ETL")

    parser.add_argument("--environment",
                        help="Shooju environment",
                        default="dev",
                        choices=["tests", "prod", "dev"])

    args, _ = parser.parse_known_args()

    if args.environment == "prod":
        args.sj_prefix = "nora\\statistics"
    elif args.environment == "tests":
        args.sj_prefix = "tests\\nora\\statistics"
    else:
        args.sj_prefix = f"users\\{SHOOJU_ENGINE.user}\\nora\\statistics"
        pass
    return args


parsed_args = parse_args()


__all__ = ["SELENIUM_HANDLER", "SHOOJU_HANDLER", "SHOOJU_ENGINE", "parsed_args"]
