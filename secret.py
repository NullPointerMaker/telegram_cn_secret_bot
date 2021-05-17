#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dbm
import re
from datetime import datetime, timedelta

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
# noinspection PyPackageRequirements
from telegram.ext import Updater, MessageHandler, Filters

with open('token') as f:
    bot = Updater(f.read().strip(), use_context=True)

lifetimeDB = dbm.open('lifetime.db', 'c')

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///job_store.db')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()


def get_member(msg):
    return str(msg.chat_id) + '@' + str(msg.from_user.id)


# noinspection PyUnusedLocal
def secret(update, context):
    if update.edited_message:
        return
    # effective message
    msg = update.effective_message
    if not msg.from_user:
        return
    # from user
    member = get_member(msg)
    lifetime = int(lifetimeDB[member])
    if not lifetime > 0:
        return
    # lifetime
    run_date = datetime.now() + timedelta(seconds=lifetime)
    job = str(msg.chat_id) + '/' + str(msg.message_id)
    scheduler.add_job(msg.delete, 'date', run_date=run_date, id=job)


def set_lifetime(msg, lifetime):
    member = get_member(msg)
    if lifetime > 0:
        lifetimeDB[member] = str(lifetime)
        msg.reply_text('你在本群发送的消息将于 ' + lifetime + ' 秒后自动删除！')
    else:
        del lifetimeDB[member]
        msg.reply_text('你在本群发送的消息将不会自动删除。')


# noinspection PyUnusedLocal
def command(update, context):
    msg = update.message
    if not msg.from_user:
        return
    # from user
    parameter = re.findall(r'^/lifetime (\d+)$', msg.text)
    if parameter:
        return set_lifetime(msg, int(parameter[0]))


bot.dispatcher.add_handler(MessageHandler(Filters.command, command))
bot.dispatcher.add_handler(MessageHandler(Filters.text, secret))

bot.start_polling()
bot.idle()
