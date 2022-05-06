# import os
# import sys
# sys.path.insert(0, './db')
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.connect_db import SessionLocal, database, engine
from db.models import Base
import uvicorn

import telebot
from telebot import types
tocken = '5171909645:AAG8HefH3P9iSSk4eMec70jBde24Vxtb3b8'
bot = telebot.TeleBot(tocken, parse_mode='HTML')



# Base.metadata.create_all(bind=engine)
db = SessionLocal()
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# db = SessionLocal()
# def get_db():
#     db = None
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()



app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/show/people")
async def show_people():
    query = f'''
    SELECT e.name , e.status, pn.position_name,  ts.date,ts.work_day_count, ws.shift_name
FROM employees e
JOIN positions pn on e.position_id = pn.id
JOIN time_sheets ts on e.id = ts.emploe_id
JOIN working_shifts ws on e.work_shift = ws.id
''' 
    #Делаем выборку с БД
    rdb = await database.fetch_all(query)
    return rdb



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/bot_add", response_class=HTMLResponse)
async def bot_add(request: Request):
    return templates.TemplateResponse("bot_add.html", {"request": request})


def ginfo():
    query = f'''
    SELECT e.name , e.status, pn.position_name,  ts.date,ts.work_day_count, ws.shift_name, br.branch_name
    FROM employees e
    JOIN positions pn on e.position_id = pn.id
    JOIN time_sheets ts on e.id = ts.emploe_id
	JOIN branches br on e.branch_id = br.id
    JOIN working_shifts ws on e.work_shift = ws.id
    '''
    r = db.execute(query)
    return r
    

menu1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn = types.KeyboardButton(text="Test")
menu1.add(btn)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
   
    bot.send_message(message.chat.id, ginfo() )
	# bot.reply_to(message, "Howdy, how are you doing?",reply_markup=menu1)



bot.infinity_polling()    

                         
                           


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8800, reload=True)
    