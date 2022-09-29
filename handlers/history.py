from aiogram import Router, F, types
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from keyboards.for_questions import get_yes_no_kb
import requests
import datetime

router = Router()


