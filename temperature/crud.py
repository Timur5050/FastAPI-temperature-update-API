from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from city.models import DBCity
from temperature.models import DBTemperature
from temperature.schemas import TemperatureSchema
from temperature.utils import get_location_key, get_city_temperature, api_key


async def set_temperature(db: AsyncSession):
    result = await db.execute(select(DBCity))
    all_city = result.scalars().all()

    for city in all_city:
        location_key = await get_location_key(city_name=city.name, api_key=api_key)
        temperature = await get_city_temperature(location_key=location_key, api_key=api_key)
        if temperature is not None:
            new_temperature = DBTemperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature,
            )
            db.add(new_temperature)
            await db.commit()
            await db.refresh(new_temperature)


def get_all_temperature(db: Session):
    return db.query(DBTemperature).all()


def get_temperature_for_city(db: Session, city_id: int):
    return db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()
