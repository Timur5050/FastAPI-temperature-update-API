from datetime import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from city.models import DBCity
from temperature.models import DBTemperature
from temperature.schemas import TemperatureSchema
from temperature.utils import get_city_temperature, api_key, get_city_temperature


async def set_temperature(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(DBCity))
        all_city = result.scalars().all()

        print(f"Found cities: {len(all_city)}")

        for city in all_city:
            temperature = await get_city_temperature(city_name=city.name)

            new_temperature = insert(DBTemperature).values(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature,
            )
            await db.execute(new_temperature)
        await db.commit()

        print(f"Added temperature: {new_temperature}")


def get_all_temperature(db: Session):
    return db.query(DBTemperature).all()


def get_temperature_for_city(db: Session, city_id: int):
    return db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()
