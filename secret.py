#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dbm
import re
from datetime import datetime, timedelta

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
# noinspection PyPackageRequirements
from telegram import Bot
# noinspection PyPackageRequirements
from telegram.ext import Updater, MessageHandler, Filters

with open('token') as f:
    token = f.read().strip()

bot = Bot(token)
updater = Updater(token, use_context=True)

lifetimeDB = dbm.open('lifetime.db', 'c')

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///job_store.db')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()


def get_member(msg):
    return '%d@%d' % (msg.chat_id, msg.from_user.id)


def delete(chat_id, message_id):
    bot.delete_message(chat_id, message_id)


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
    args = [msg.chat_id, msg.message_id]
    run_date = datetime.now() + timedelta(seconds=lifetime)
    job = '%d/%d' % (msg.chat_id, msg.message_id)
    scheduler.add_job(delete, 'date', run_date=run_date, args=args, id=job)


def set_lifetime(msg, lifetime):
    member = get_member(msg)
    if lifetime > 0:
        lifetimeDB[member] = str(lifetime)
        msg.reply_text('你在群内所发消息将于 %d 秒后自动删除！' % lifetime)
    else:
        del lifetimeDB[member]
        msg.reply_text('你在群内所发消息将不自动删除。')


# noinspection PyUnusedLocal
def command(update, context):
    msg = update.message
    if not msg.from_user:
        return
    # from user
    parameter = re.findall(r'^/lifetime (\d+)$', msg.text)
    if parameter:
        return set_lifetime(msg, int(parameter[0]))


updater.dispatcher.add_handler(MessageHandler(Filters.command, command))
updater.dispatcher.add_handler(MessageHandler(Filters.text, secret))

updater.start_polling()
updater.idle()
