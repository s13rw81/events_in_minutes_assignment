import logging

import motor.motor_asyncio
from beanie import init_beanie
from config import DATABASE_URL, DATABASE_PORT, DATABASE_NAME
from logging_config import log
from models.bookings.bookings_internal import BookingsInternal
from models.user.user_external import UserExternal
from models.user.user_internal import UserInternal

CONNECTION_STRING = f"mongodb://{DATABASE_URL}:{DATABASE_PORT}"


async def init_db():
    log.info(f'initializing database with connection string {CONNECTION_STRING}')
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
    await init_beanie(database=client[DATABASE_NAME], document_models=[UserInternal, UserExternal, BookingsInternal])
    await UserInternal.get_motor_collection().create_index("username", unique=True)
    await UserInternal.get_motor_collection().create_index("email", unique=True)
    log.info('database initialized successfully.')
