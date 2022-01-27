# Imports
from enum import Enum
import datetime
from dateutil.relativedelta import relativedelta


class Hemisphere(Enum):
    NORTH = "n"
    SOUTH = "s"

    def calculate_current_month(self) -> str:
        if self == self.NORTH.value:
            return datetime.datetime.now().strftime("%B")
        else:
            return (datetime.datetime.now() + relativedelta(months=6)).strftime("%B")

    @staticmethod
    def convert_text_to_hemisphere(text: str):
        """
        Take text and convert it into a valid hemisphere
        """
        # Sanitise the input
        clean_text = text.strip().lower()
        if clean_text == Hemisphere.SOUTH.value:
            return Hemisphere.SOUTH
        else:
            return Hemisphere.NORTH
