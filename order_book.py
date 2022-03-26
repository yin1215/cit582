from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import copy

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #Your code here
    fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount']
    new_order = Order(**{f: order[f] for f in fields})
    session.add(new_order)
    session.commit()

    for existing_order in session.query(Order).filter(Order.creator == None).all():
        if existing_order.filled is not None:
            continue
        if existing_order.buy_currency != new_order.sell_currency:
            continue
        if existing_order.sell_currency != new_order.buy_currency:
            continue
        if existing_order.sell_amount / existing_order.buy_amount < new_order.buy_amount/new_order.sell_amount:
            continue

        timestamp = datetime.utcnow()
        new_order.filled = timestamp
        existing_order.filled = timestamp
        new_order.counterparty_id, existing_order.counterparty_id = existing_order.id, new_order.id
        session.commit()

        fields.append('creator_id')

        if new_order.sell_amount > existing_order.buy_amount:
            order_child = copy.deepcopy(order)
            order_child['buy_amount'] = (new_order.sell_amount - existing_order.buy_amount) * new_order.buy_amount/new_order.sell_amount
            order_child['sell_amount'] = new_order.sell_amount - existing_order.buy_amount
            order_child['creator_id'] = new_order.id
            child_order = Order(**{f: order_child[f] for f in fields})
            session.add(child_order)
            session.commit()

        elif new_order.sell_amount < existing_order.buy_amount:
            order_child = {}
            order_child['sender_pk'] = existing_order.sender_pk
            order_child['receiver_pk'] = existing_order.receiver_pk
            order_child['buy_currency'] = existing_order.buy_currency
            order_child['sell_currency'] = existing_order.sell_currency
            order_child['buy_amount'] = existing_order.buy_amount - new_order.sell_amount
            order_child['sell_amount'] = (existing_order.buy_amount - new_order.sell_amount) * existing_order.sell_amount / existing_order.buy_amount
            order_child['creator_id'] = existing_order.id
            child_order = Order(**{f: order_child[f] for f in fields})
            session.add(child_order)
            session.commit()

        break

    return
