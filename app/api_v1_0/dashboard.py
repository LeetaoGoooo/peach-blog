from flask import request, jsonify
from . import api
from app.models import Comment, MessageBoard, PostView, History
import datetime
from sqlalchemy import func

def get_comment_count():
    comment_count = Comment.query.all().count()
    return comment_count

def get_message_board_count():
    message_board_count = MessageBoard.query.all().count()
    return message_board_count


def get_today_visit_count():
    today_visit_count = PostView.query.filter_by(visit_date=datetime.datetime.today()).with_entities(func.sum(PostView.views)).all()
    return today_visit_count

def get_sum_visit_count():
    sum_visit_count = PostView.query.with_entities(func.sum(PostView.views)).all()
    return sum_visit_count

def get_today_visit_chart():
    rows = History.query(func.count(History.id).label("count"),func.date_format(History.visit_time,"%Y-%m-%d %H").label("today_time")).group_by(func.date_format(History.visit_time,"%Y-%m-%d %H"))
    today_visit_data_dict = {}
    for row in rows:
        print(row.count,row.today_time)
    return rows

@api.route("/dashboard", methods=["GET"])
def dashboard():
    return jsonify(get_today_visit_chart())


        