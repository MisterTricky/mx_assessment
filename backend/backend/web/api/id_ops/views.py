from datetime import datetime, date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.db.dependencies import get_db_session
from backend.models.id_search import IDSearch, Holiday
from backend.schemas.id_search import IDSearchResponse
from backend.services.id_validator import IDValidator
from backend.services.calendarific.holiday_service import HolidayService

router = APIRouter()
holiday_service = HolidayService()

@router.post("/validate")
async def validate_id(
    request: Request,
    id_number: str = Form(...),
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Validate a South African ID number and return its decoded information
    along with any associated holidays and additional birth date insights.
    """
    # Validate ID number format first
    if not IDValidator.validate_id_number(id_number):
        raise HTTPException(
            status_code=400,
            detail="Invalid ID number format"
        )

    # Decode ID number components
    id_info = await IDValidator.decode_id_number(id_number)
    
    # Extract birth date from ID number
    birth_date = id_info["date_of_birth"]

    # Calculate last and next birthday
    today = date.today()
    current_year = today.year
    birthday_this_year = birth_date.replace(year=current_year).date()
    
    if birthday_this_year > today:
        last_birthday = birth_date.replace(year=current_year - 1).date()
        next_birthday = birthday_this_year
    else:
        last_birthday = birthday_this_year
        next_birthday = birth_date.replace(year=current_year + 1).date()

    # Check if birthdays fall on holidays
    last_birthday_holiday = await holiday_service.is_public_holiday(datetime.combine(last_birthday, datetime.min.time()))
    next_birthday_holiday = await holiday_service.is_public_holiday(datetime.combine(next_birthday, datetime.min.time()))

    # Fetch holidays around the birthday
    holidays_around_birthday = await holiday_service.get_holidays_around_birthday(birth_date)

    # Get holidays for the birth date
    stmt = select(IDSearch).options(selectinload(IDSearch.holidays)).where(IDSearch.id_number == id_number)
    result = await db.execute(stmt)
    search = result.scalar_one_or_none()

    if not search:
        search = IDSearch(
            id_number=id_number,
            date_of_birth=id_info["date_of_birth"],
            gender=id_info["gender"],
            is_citizen=id_info["citizen"]
        )
        db.add(search)
        await db.commit()
        await db.refresh(search)

    # Format response with additional information
    response = {
        "id_info": {
            "date_of_birth": id_info["date_of_birth"].strftime("%Y-%m-%d"),
            "gender": id_info["gender"],
            "citizen_status": "South African Citizen" if id_info["citizen"] else "Permanent Resident",
            "age": id_info["age"],
        },
        "birth_insights": {
            "day_of_week": id_info["day_of_week"],
            "zodiac": {
                "western": id_info["zodiac_sign"],
                "chinese": id_info["chinese_zodiac"]
            },
            "birth_symbols": {
                "stone": {
                    "name": id_info["birth_stone"]["name"],
                    "meaning": id_info["birth_stone"]["meaning"],
                    "color": id_info["birth_stone"]["color"]
                },
                "flower": {
                    "name": id_info["birth_flower"]["name"],
                    "meaning": id_info["birth_flower"]["meaning"],
                    "colors": id_info["birth_flower"]["colors"]
                }
            },
            "numerology": {
                "life_path_number": id_info["life_path_number"],
                "meaning": id_info["life_path_meaning"]
            },
            "birthday_countdown": {
                "days_remaining": id_info["days_to_next_birthday"],
                "is_today": id_info["is_birthday_today"]
            },
            "shared_birthdays": id_info["famous_birthdays"]
        },
        "holidays": [
            {
                "name": holiday.name,
                "description": holiday.description,
                "date": holiday.date.strftime("%Y-%m-%d")
            }
            for holiday in (search.holidays or [])
        ],
        "holidays_around_birthday": [
            {
                "name": holiday["name"],
                "description": holiday["description"],
                "date": datetime(**holiday["date"]["datetime"]).strftime("%Y-%m-%d")
            }
            for holiday in holidays_around_birthday
        ],
        "last_birthday": {
            "date": last_birthday.isoformat(),
            "holiday": holiday_service.format_holiday(last_birthday_holiday) if last_birthday_holiday else None
        },
        "next_birthday": {
            "date": next_birthday.isoformat(),
            "holiday": holiday_service.format_holiday(next_birthday_holiday) if next_birthday_holiday else None
        }
    }

    # Add special messages
    special_messages = []
    
    if id_info["is_birthday_today"]:
        special_messages.append("🎉 Happy Birthday! 🎂")
    
    if id_info["famous_birthdays"]:
        special_messages.append(f"You share your birthday with {', '.join(id_info['famous_birthdays'])}! 🌟")

    # Add birth symbols message
    birth_stone = id_info["birth_stone"]["name"]
    birth_flower = id_info["birth_flower"]["name"]
    special_messages.append(f"Your birth stone is the {birth_stone} 💎 and your birth flower is the {birth_flower} 🌸")
    
    if special_messages:
        response["special_messages"] = special_messages

    return response

# Legacy endpoint - can be removed if not needed
@router.get("/validate/{id_number}", response_model=IDSearchResponse)
async def validate_id_get(id_number: str, db: AsyncSession = Depends(get_db_session)):
    """
    Legacy endpoint for backward compatibility.
    Consider using the POST /validate endpoint for new integrations.
    """
    # Validate ID number format
    if not IDValidator.validate_id_number(id_number):
        raise HTTPException(status_code=400, detail="Invalid ID number format")

    # Check if ID has been searched before - include holidays relationship
    query = select(IDSearch).where(IDSearch.id_number == id_number).options(selectinload(IDSearch.holidays))
    result = await db.execute(query)
    existing_search = result.scalar_one_or_none()

    # Decode ID number
    id_info = await IDValidator.decode_id_number(id_number)

    if existing_search:
        # Update search count
        existing_search.search_count += 1
        existing_search.updated_at = datetime.utcnow()
        await db.commit()
        
        return IDSearchResponse(
            id_number=id_number,
            date_of_birth=existing_search.date_of_birth.strftime("%Y-%m-%d"),
            gender=existing_search.gender,
            citizen=existing_search.citizen,
            search_count=existing_search.search_count,
            holidays=existing_search.holidays
        )

    # Create new ID search record
    new_search = IDSearch(
        id_number=id_number,
        date_of_birth=id_info["date_of_birth"],
        gender=id_info["gender"],
        citizen=id_info["citizen"],
        search_count=1,
        created_at=datetime.utcnow()
    )
    
    db.add(new_search)
    await db.commit()
    await db.refresh(new_search)

    return IDSearchResponse(
        id_number=id_number,
        date_of_birth=new_search.date_of_birth.strftime("%Y-%m-%d"),
        gender=new_search.gender,
        citizen=new_search.citizen,
        search_count=new_search.search_count,
        holidays=[]
    )
