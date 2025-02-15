from quart import Quart, request, jsonify
from CheckerService.Checker import check_comics
from CheckerService.Logger import Logger

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

    try:
        logger.info(f"Checking comics")
        result = await check_comics(title)
        logger.info(f"Result: {result}")
        return jsonify({"result": result})
    except Exception as e:
        logger.error(f"Error checking comics: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/health", methods=["GET"])
async def health_check():
    return jsonify({"status": "healthy"})
