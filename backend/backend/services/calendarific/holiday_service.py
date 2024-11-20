from datetime import datetime
import os
from typing import List, Optional
from .service import CalendarificService
from ..cache_service import cache_response

class HolidayService:
    def __init__(self):
        api_key = os.getenv("BACKEND_CALENDARIFIC_API_KEY")
        if not api_key:
            raise ValueError("CALENDARIFIC_API_KEY environment variable is not set")
        self.calendarific = CalendarificService(api_key)

    @cache_response(ttl=3600 * 24)  # Cache for 24 hours
    async def get_holidays_for_year(self, year: int, country_code: str = "ZA") -> List[dict]:
        """
        Fetches public holidays for a specific year and country.
        Results are cached for 24 hours.
        """
        try:
            return await self.calendarific.get_holidays(year, country_code)
        except Exception as e:
            print(f"Error fetching holidays: {e}")
            return []

    @cache_response(ttl=3600 * 24)  # Cache for 24 hours
    async def get_holidays_for_date(self, date: datetime, country_code: str = "ZA") -> List[dict]:
        """
        Gets holidays that match a specific date.
        Results are cached for 24 hours.
        """
        year_holidays = await self.get_holidays_for_year(date.year, country_code)
        return [
            holiday for holiday in year_holidays
            if datetime.fromisoformat(holiday["date"]["iso"]).date() == date.date()
        ]

    @cache_response(ttl=3600 * 24)  # Cache for 24 hours
    async def get_holidays_around_birthday(self, birthday: datetime, country_code: str = "ZA") -> List[dict]:
        """
        Fetches public holidays for the month before, the month of, and the month after the given birthday.
        Results are cached for 24 hours.
        """
        holidays = []
        months_to_check = [birthday.month - 1, birthday.month, birthday.month + 1]
        years_to_check = list(set([birthday.year if month > 0 else birthday.year - 1 for month in months_to_check] +
                                [birthday.year if month < 13 else birthday.year + 1 for month in months_to_check]))

        # Adjust months that fall outside the 1-12 range
        adjusted_months = [(month + 12 if month < 1 else month - 12 if month > 12 else month) for month in months_to_check]

        for year in years_to_check:
            # Fetch all holidays for the year
            yearly_holidays = await self.calendarific.get_holidays(year, country_code)
            
            # Filter holidays for the relevant months
            for holiday in yearly_holidays:
                holiday_date = datetime.fromisoformat(holiday["date"]["iso"])
                if holiday_date.month in adjusted_months:
                    holidays.append(holiday)

        return holidays

    @cache_response(ttl=3600 * 24)  # Cache for 24 hours
    async def is_public_holiday(self, date: datetime, country_code: str = "ZA") -> Optional[dict]:
        """
        Checks if a given date is a public holiday.
        Returns the holiday information if it is, None otherwise.
        Results are cached for 24 hours.
        """
        holidays = await self.get_holidays_for_date(date, country_code)
        return holidays[0] if holidays else None

    def format_holiday(self, holiday: dict) -> dict:
        """
        Formats a holiday response from the Calendarific API into our schema format.
        """
        return {
            "name": holiday["name"],
            "description": holiday.get("description", None),
            "date": datetime.fromisoformat(holiday["date"]["iso"]),
            "type": holiday.get("type", [None])[0]
        }

    async def close(self):
        """
        Closes the underlying Calendarific service.
        Should be called when the service is no longer needed.
        """
        await self.calendarific.close()
