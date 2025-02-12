from flask import Flask, request, jsonify
from ComicsLibrary.orchestrators import Orchestrator
from ComicsLibrary.DTO import UserDTO, ComicDTO
from ComicsLibrary.loggers.Logger import Logger
from dataclasses import asdict
from typing import List

app = Flask(__name__)
orchestrator = Orchestrator()
logger = Logger.get_logger("Controller")


def dto_to_dict(dto):
    return asdict(dto)


@app.route("/user/", methods=["POST"])
def add_user():
    user_data = request.get_json()
    logger.info(f"Adding user {user_data}")
    user_dto = orchestrator.add_user(UserDTO(**user_data))
    logger.info(f"Return user {user_dto}")
    if user_dto is None:
        return {"result": None}
    return jsonify(dto_to_dict(user_dto))


@app.route("/comic/", methods=["POST"])
def add_comic():
    comic_data = request.get_json()
    logger.info(f"Adding comic {comic_data}")
    comic_dto = orchestrator.add_comic(ComicDTO(**comic_data))
    logger.info(f"Return comic {comic_dto}")
    if comic_dto is None:
        return {"result": None}
    return jsonify(dto_to_dict(comic_dto))


@app.route("/comic/", methods=["GET"])
def get_comic():
    comic_data = request.get_json()
    logger.info(f"Getting comic {comic_data}")
    comic = ComicDTO(**comic_data)
    comic_dto = orchestrator.get_comic(id=comic.id, title=comic.title)
    logger.info(f"Return comic {comic_dto}")
    if comic_dto is None:
        return {"result": None}
    return jsonify(dto_to_dict(comic_dto))


@app.route("/user/", methods=["GET"])
def get_user():
    user_data = request.get_json()
    logger.info(f"Getting comic {user_data}")
    user = UserDTO(**user_data)
    user_dto = orchestrator.get_user(chat_id=user.chat_id, id=user.id)
    logger.info(f"Return user {user_dto}")
    if user_dto is None:
        return {"result": None}
    return jsonify(dto_to_dict(user_dto))


@app.route("/comics/all", methods=["GET"])
def get_comics():
    logger.info("Getting comics")
    comics_dto = orchestrator.get_comics()
    logger.info("Return comics")
    return jsonify([dto_to_dict(comic) for comic in comics_dto])


@app.route("/user/<int:chat_id>/comics/<string:comic_id>", methods=["POST"])
def add_comic_to_user(chat_id: int, comic_id: str):
    logger.info(f"Adding comic {comic_id} to user {chat_id}")
    status = orchestrator.add_comic_to_user(comic_id, chat_id)
    return jsonify({"result": status})