from quart import Quart, request, jsonify
from Checker.Checker import check_comics
import asyncio
from Checker.Logger import Logger

app = Quart(__name__)
logger = Logger.get_logger(__name__)
@app.route("/comics/check", methods=["GET"])
async def check_user():
    logger.info("Checking comics")
    title = request.args.get("title")
    logger.info(f"Title: {title}")
    if not title:
        logger.error("Title not found")
        return jsonify({"error": "Title is required"}), 400
    result = await check_comics(title)
    logger.info(f"Result: {result}")
    return jsonify({"result": result})

@app.route("/health", methods=["GET"])
async def health_check():
    return jsonify({"status": "healthy"})
