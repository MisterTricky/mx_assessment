import httpx
from typing import List, Dict, Any
from datetime import datetime

class CalendarificService:
    """
    Service for interacting with the Calendarific API to fetch holiday information.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://calendarific.com/api/v2"
        self.client = httpx.AsyncClient()

    async def get_holidays(self, year: int, country: str = "ZA") -> List[Dict[str, Any]]:
        """
        Fetches holidays for a specific year and country.
        
        Args:
            year (int): The year to fetch holidays for
            country (str): The country code (default: "ZA" for South Africa)
            
        Returns:
            List[Dict[str, Any]]: List of holidays with their details
        """
        endpoint = f"{self.base_url}/holidays"
        
        params = {
            "api_key": self.api_key,
            "country": country,
            "year": year,
            "type": "national,local,religious"
        }
        
        try:
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data["meta"]["code"] != 200:
                raise ValueError(f"API Error: {data['meta']['error_type']}")
            
            holidays = data["response"]["holidays"]
            
            # Add ISO formatted date to each holiday
            for holiday in holidays:
                holiday["date"]["iso"] = self.format_date(holiday["date"])
                
            return holidays
            
        except httpx.RequestError as e:
            raise Exception(f"Failed to fetch holidays: {str(e)}")
        except (KeyError, ValueError) as e:
            raise Exception(f"Error processing API response: {str(e)}")

    def format_date(self, date_obj: Dict[str, Any]) -> str:
        """
        Formats a date object from the API response into ISO format.
        
        Args:
            date_obj (Dict[str, Any]): Date object from API response
            
        Returns:
            str: ISO formatted date string
        """
        try:
            # The API returns a 'datetime' object within the date_obj
            datetime_obj = date_obj.get("datetime", {})
            
            # Extract year, month, and day from the datetime object
            year = int(datetime_obj.get("year", date_obj.get("year")))
            month = int(datetime_obj.get("month", date_obj.get("month")))
            day = int(datetime_obj.get("day", date_obj.get("day")))
            
            dt = datetime(year=year, month=month, day=day)
            return dt.isoformat()
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format in API response: {str(e)}")

    async def close(self):
        """
        Closes the HTTP client session.
        Should be called when the service is no longer needed.
        """
        await self.client.aclose()
