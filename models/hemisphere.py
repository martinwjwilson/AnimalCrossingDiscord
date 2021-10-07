import enum
import datetime
from dateutil.relativedelta import relativedelta


class Hemisphere(enum):
    NORTH = "n"
    SOUTH = "s"

    def calculate_current_month(self) -> str:
        if self == Hemisphere.NORTH.value:
            return datetime.datetime.now().strftime("%B")
        else:
            return (datetime.datetime.now() + relativedelta(months=6)).strftime("%B")
