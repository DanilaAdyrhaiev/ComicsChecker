from quart import Quart, request, jsonify
from CheckerService.Checker import check_comics
from CheckerService.Logger import Logger

app = Quart(__name__)
logger = Logger.get_logger(__name__)


@app.route("/comics/check", methods=["GET"])
async def check_user():
    logger.info(f"RAW QUERY STRING: {request.query_string.decode('utf-8')}")
    title = request.args.get("title")
    logger.info(f"Received request to check comics with title: {title}")
    if not title:
        logger.error("Title parameter is missing")
        return jsonify({"error": "Title is required"}), 400

    try:
        logger.info(f"Checking comics for title: {title}")
        result = await check_comics(title)
        logger.info(f"Check result: {result}")
        return jsonify({"result": result})
    except Exception as e:
        logger.exception("Unhandled exception while checking comics")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/health", methods=["GET"])
async def health_check():
    return jsonify({"status": "healthy"})
