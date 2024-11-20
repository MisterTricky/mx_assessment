from datetime import datetime
import calendar
from typing import Dict, Any
from .cache_service import cache_response

class IDValidator:
    CHINESE_ZODIAC = [
        "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]

    BIRTH_MONTHS = {
        1: {
            "stone": {
                "name": "Garnet",
                "meaning": "Represents faith, love and constancy",
                "color": "Deep Red"
            },
            "flower": {
                "name": "Carnation",
                "meaning": "Love, fascination, and distinction",
                "colors": ["Pink", "Red", "White"]
            }
        },
        2: {
            "stone": {
                "name": "Amethyst",
                "meaning": "Brings peace, tranquility and protection",
                "color": "Purple"
            },
            "flower": {
                "name": "Violet",
                "meaning": "Modesty, virtue, and faithfulness",
                "colors": ["Purple", "White"]
            }
        },
        3: {
            "stone": {
                "name": "Aquamarine",
                "meaning": "Brings courage, calmness and protection",
                "color": "Blue-Green"
            },
            "flower": {
                "name": "Daffodil",
                "meaning": "Rebirth, new beginnings, and eternal life",
                "colors": ["Yellow", "White"]
            }
        },
        4: {
            "stone": {
                "name": "Diamond",
                "meaning": "Represents innocence, love and fidelity",
                "color": "Clear"
            },
            "flower": {
                "name": "Daisy",
                "meaning": "Innocence, purity, and true love",
                "colors": ["White", "Yellow"]
            }
        },
        5: {
            "stone": {
                "name": "Emerald",
                "meaning": "Symbolizes love, rebirth and wisdom",
                "color": "Green"
            },
            "flower": {
                "name": "Lily of the Valley",
                "meaning": "Return of happiness, humility, and sweetness",
                "colors": ["White"]
            }
        },
        6: {
            "stone": {
                "name": "Pearl",
                "meaning": "Represents purity, integrity and love",
                "color": "White"
            },
            "flower": {
                "name": "Rose",
                "meaning": "Love, gratitude, and appreciation",
                "colors": ["Red", "Pink", "White"]
            }
        },
        7: {
            "stone": {
                "name": "Ruby",
                "meaning": "Brings love, success and integrity",
                "color": "Red"
            },
            "flower": {
                "name": "Larkspur",
                "meaning": "Strong bonds of love and an open heart",
                "colors": ["Purple", "Pink", "White"]
            }
        },
        8: {
            "stone": {
                "name": "Peridot",
                "meaning": "Brings good fortune, peace and success",
                "color": "Light Green"
            },
            "flower": {
                "name": "Gladiolus",
                "meaning": "Strength of character, moral integrity",
                "colors": ["Red", "Pink", "Purple", "White"]
            }
        },
        9: {
            "stone": {
                "name": "Sapphire",
                "meaning": "Represents wisdom, virtue and good fortune",
                "color": "Blue"
            },
            "flower": {
                "name": "Aster",
                "meaning": "Love, faith, and wisdom",
                "colors": ["Purple", "White"]
            }
        },
        10: {
            "stone": {
                "name": "Opal",
                "meaning": "Brings hope, creativity and innocence",
                "color": "Multicolor"
            },
            "flower": {
                "name": "Marigold",
                "meaning": "Creativity, passion, and sacred offering",
                "colors": ["Orange", "Yellow"]
            }
        },
        11: {
            "stone": {
                "name": "Topaz",
                "meaning": "Symbolizes love, affection and purpose",
                "color": "Yellow"
            },
            "flower": {
                "name": "Chrysanthemum",
                "meaning": "Joy, optimism, and long life",
                "colors": ["Red", "Yellow", "White"]
            }
        },
        12: {
            "stone": {
                "name": "Turquoise",
                "meaning": "Brings prosperity, success and happiness",
                "color": "Blue-Green"
            },
            "flower": {
                "name": "Narcissus",
                "meaning": "Hope, wealth, and good fortune",
                "colors": ["White", "Yellow"]
            }
        }
    }

    FAMOUS_BIRTHDAYS = {
        "01-01": ["Verne Troyer", "Frank Langella"],
        "02-02": ["Shakira", "Christie Brinkley"],
        "03-03": ["Alexander Graham Bell", "Jessica Biel"],
        "04-04": ["Robert Downey Jr.", "Heath Ledger"],
        "05-05": ["Adele", "Chris Brown"],
        "06-06": ["Jason Isaacs", "Paul Giamatti"],
        "07-07": ["Ringo Starr", "Jim Gaffigan"],
        "08-08": ["Roger Federer", "Dustin Hoffman"],
        "09-09": ["Adam Sandler", "Hugh Grant"],
        "10-10": ["David Lee Roth", "Brett Favre"],
        "11-11": ["Leonardo DiCaprio", "Demi Moore"],
        "12-12": ["Frank Sinatra", "Bob Barker"],
        "12-25": ["Annie Lennox", "Justin Trudeau"]
    }

    @staticmethod
    def get_zodiac_sign(date: datetime) -> str:
        """Get zodiac sign based on birth date."""
        day = date.day
        month = date.month
        
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        else:
            return "Pisces"

    @staticmethod
    def get_chinese_zodiac(year: int) -> str:
        """Get Chinese zodiac animal based on birth year."""
        return IDValidator.CHINESE_ZODIAC[year % 12]

    @staticmethod
    def get_life_path_number(date: datetime) -> dict:
        """Calculate life path number based on birth date."""
        def reduce_to_single_digit(n: int) -> int:
            while n > 9:
                n = sum(int(d) for d in str(n))
            return n

        year = reduce_to_single_digit(sum(int(d) for d in str(date.year)))
        month = reduce_to_single_digit(date.month)
        day = reduce_to_single_digit(date.day)
        
        life_path = reduce_to_single_digit(year + month + day)
        
        meanings = {
            1: "The Leader: Independent, focused, and a natural-born leader",
            2: "The Mediator: Diplomatic, sensitive, and cooperative",
            3: "The Creative: Expressive, optimistic, and talented in arts",
            4: "The Worker: Practical, trustworthy, and hardworking",
            5: "The Freedom Seeker: Adventurous, versatile, and progressive",
            6: "The Nurturer: Responsible, caring, and a natural healer",
            7: "The Seeker: Analytical, introspective, and philosophical",
            8: "The Powerhouse: Ambitious, successful, and materialistic",
            9: "The Humanitarian: Compassionate, romantic, and selfless"
        }
        
        return {
            "number": life_path,
            "meaning": meanings.get(life_path, "Unknown meaning")
        }

    @staticmethod
    def get_birth_day_info(date: datetime) -> dict:
        """Get information about the day of birth."""
        day_name = calendar.day_name[date.weekday()]
        month_day = date.strftime("%m-%d")
        famous_people = IDValidator.FAMOUS_BIRTHDAYS.get(month_day, [])
        
        return {
            "day_of_week": day_name,
            "famous_birthdays": famous_people
        }

    @staticmethod
    def get_birth_symbols(date: datetime) -> dict:
        """Get birth stone and flower information based on birth month."""
        month_info = IDValidator.BIRTH_MONTHS[date.month]
        return {
            "stone": month_info["stone"],
            "flower": month_info["flower"]
        }

    @staticmethod
    def calculate_age(birth_date: datetime) -> dict:
        """Calculate age and additional age-related information."""
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Calculate next birthday
        this_year_birthday = birth_date.replace(year=today.year)
        if this_year_birthday < today:
            next_birthday = birth_date.replace(year=today.year + 1)
        else:
            next_birthday = this_year_birthday
        
        days_to_birthday = (next_birthday - today).days
        
        return {
            "years": age,
            "days_to_next_birthday": days_to_birthday,
            "is_birthday_today": days_to_birthday == 0
        }

    @staticmethod
    def validate_id_number(id_number: str) -> bool:
        """
        Validates a South African ID number based on the official format.
        """
        # Basic length check
        if len(id_number) != 13 or not id_number.isdigit():
            return False

        try:
            # Extract components
            birth_year = int(id_number[0:2])
            birth_month = int(id_number[2:4])
            birth_day = int(id_number[4:6])
            gender = int(id_number[6:10])
            citizenship = int(id_number[10])
            checksum = int(id_number[12])

            # Validate date components
            if birth_month < 1 or birth_month > 12:
                return False
            if birth_day < 1 or birth_day > 31:
                return False

            # Validate citizenship
            if citizenship not in [0, 1]:
                return False

            # Validate checksum (Luhn algorithm)
            return IDValidator._validate_checksum(id_number)

        except ValueError:
            return False

    @staticmethod
    @cache_response(ttl=3600 * 24)  # Cache for 24 hours
    async def decode_id_number(id_number: str) -> Dict[str, Any]:
        """
        Decodes a South African ID number into its components.
        Results are cached for 24 hours since ID information doesn't change.
        """
        birth_year = int(id_number[0:2])
        birth_month = int(id_number[2:4])
        birth_day = int(id_number[4:6])
        gender_num = int(id_number[6:10])
        citizenship = int(id_number[10])

        # Determine century
        # For SA ID numbers, if the year is greater than current year, it's from previous century
        current_year = datetime.now().year % 100
        century = 1900 if birth_year > current_year else 2000

        # Create full date
        date_of_birth = datetime(century + birth_year, birth_month, birth_day)
        
        # Get additional information
        age_info = IDValidator.calculate_age(date_of_birth)
        zodiac_sign = IDValidator.get_zodiac_sign(date_of_birth)
        chinese_zodiac = IDValidator.get_chinese_zodiac(date_of_birth.year)
        life_path_number = IDValidator.get_life_path_number(date_of_birth)
        birth_day_info = IDValidator.get_birth_day_info(date_of_birth)
        birth_symbols = IDValidator.get_birth_symbols(date_of_birth)

        return {
            "date_of_birth": date_of_birth,
            "gender": "male" if gender_num >= 5000 else "female",
            "citizen": citizenship == 0,
            "age": age_info["years"],
            "days_to_next_birthday": age_info["days_to_next_birthday"],
            "is_birthday_today": age_info["is_birthday_today"],
            "zodiac_sign": zodiac_sign,
            "chinese_zodiac": chinese_zodiac,
            "life_path_number": life_path_number["number"],
            "life_path_meaning": life_path_number["meaning"],
            "day_of_week": birth_day_info["day_of_week"],
            "famous_birthdays": birth_day_info["famous_birthdays"],
            "birth_stone": birth_symbols["stone"],
            "birth_flower": birth_symbols["flower"]
        }

    @staticmethod
    def _validate_checksum(id_number: str) -> bool:
        """
        Validates the ID number using the Luhn algorithm.
        """
        # Multiply every second digit by 2
        total = 0
        for i in range(len(id_number)):
            digit = int(id_number[i])
            if i % 2 == 1:  # odd position
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        return total % 10 == 0
