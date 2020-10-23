from flask import request, jsonify
from . import api
from app.models import Comment, MessageBoard, PostView, History, Post
import datetime
from sqlalchemy import func
from collections import OrderedDict
from pathlib import Path
import time


def get_certain_day_sum_visit_count(visit_date):
    certain_day_visit_res = PostView.query.filter_by(
        visit_date=visit_date.strftime("%Y-%m-%d")).with_entities(
        func.sum(PostView.views).label("certain_day_visit_count")).all()
    return certain_day_visit_res[0].certain_day_visit_count if certain_day_visit_res[
                                                                   0].certain_day_visit_count is not None else 0


def get_comment_count():
    comment_count = Comment.query.count()
    return comment_count


def get_message_board_count():
    message_board_count = MessageBoard.query.count()
    return message_board_count


def get_today_visit_count():
    return get_certain_day_sum_visit_count(datetime.datetime.today())


def get_sum_visit_count():
    sum_visit_res = PostView.query.with_entities(
        func.sum(PostView.views).label("sum_visit_count")).all()
    return sum_visit_res[0].sum_visit_count if sum_visit_res[0].sum_visit_count is not None else 0


def get_init_today_visit_data_dict():
    key_prefix = datetime.datetime.today().strftime("%Y-%m-%d")
    today_visit_data_dict = OrderedDict()
    for i in range(24):
        if i < 10:
            key_suffix = "0{}".format(i)
        else:
            key_suffix = str(i)
        key = "{} {}:00".format(key_prefix, key_suffix)
        today_visit_data_dict[key] = 0
    return today_visit_data_dict


def get_today_visit_chart():
    visit_time_like = "{}%".format(
        datetime.datetime.today().strftime("%Y-%m-%d"))
    rows = History.query.filter(History.visit_time.like(visit_time_like)).with_entities(func.count(History.id).label(
        "count"), func.date_format(History.visit_time, "%Y-%m-%d %H").label("today_time")).group_by(
        func.date_format(History.visit_time, "%Y-%m-%d %H"))
    today_visit_data_dict = get_init_today_visit_data_dict()
    for row in rows:
        key = "{}:00".format(row.today_time)
        today_visit_data_dict[key] = row.count
    today_visit_chart_data_dict = {}
    today_visit_chart_data_dict["xAxis"] = list(today_visit_data_dict.keys())
    today_visit_chart_data_dict["series"] = list(
        today_visit_data_dict.values())
    return today_visit_chart_data_dict


def get_top_ten_posts():
    rows = Post.query.join(PostView, Post.id == PostView.post_id).with_entities(func.sum(PostView.views).label(
        "sum_views"), Post.id, Post.title).group_by(PostView.post_id).order_by(func.sum(PostView.views).desc()).limit(
        10)
    top_ten_post_list = []
    for row in rows:
        top_ten_post_list.append([row.id, row.title])
    return top_ten_post_list


def get_sum_seven_day_visit_chart():
    seven_day_visit_xAxis_list = []
    sever_day_visit_series_list = []
    today = datetime.datetime.now()
    for i in range(7):
        sub_day = i - 6
        certain_day = (datetime.datetime.now() +
                       datetime.timedelta(days=sub_day))
        seven_day_visit_xAxis_list.append(certain_day.strftime("%Y-%m-%d"))
        sever_day_visit_series_list.append(
            get_certain_day_sum_visit_count(certain_day))
    sum_seven_day_visit_chart_data_dict = {}
    sum_seven_day_visit_chart_data_dict['xAxis'] = seven_day_visit_xAxis_list
    sum_seven_day_visit_chart_data_dict['series'] = sever_day_visit_series_list
    return sum_seven_day_visit_chart_data_dict


def get_sum_device_visit_chart():
    rows = History.query.with_entities(func.count(History.id).label(
        "device_count"), History.browser).group_by(History.browser)
    sum_device_visit_data_list = []
    for row in rows:
        temp_dict = {}
        temp_dict['name'] = row.browser
        temp_dict['value'] = row.device_count
        sum_device_visit_data_list.append(temp_dict)
    return sum_device_visit_data_list


def get_unread_comments():
    rows = Comment.query.filter_by(is_read=0).all()
    return len(rows)


@api.route("/dashboard", methods=["GET"])
def dashboard():
    # https://github.com/pallets/flask/issues/835
    return jsonify({"comment_count": get_comment_count(), "message_board_count": get_message_board_count(),
                    "today_visit_count": get_today_visit_count(), "sum_visit_count": get_sum_visit_count(),
                    "today_visit_chart": get_today_visit_chart(), "top_ten_posts": get_top_ten_posts(),
                    "sum_seven_day_visit_chart": get_sum_seven_day_visit_chart(),
                    "sum_device_visit": get_sum_device_visit_chart(), "unread_comments": get_unread_comments()})


@api.route("/image", methods=["POST"])
def upload_image():
    image = request.files.get('editormd-image-file')
    ext = image.filename.split(".")[-1]
    root_path = Path.joinpath(Path.cwd(), 'app', 'static', 'posts')
    if not Path.exists(root_path):
        Path.mkdir(root_path)
    file_name = f'{str(int(time.time()))}.{ext}'
    file_path = Path.joinpath(root_path, file_name)
    try:
        image.save(str(file_path))
    except Exception as e:
        return jsonify({"success": 0, "message": str(e), "url": ""})
    return jsonify({"success": 1, "message": "", "url": f'/posts/{file_name}'})
