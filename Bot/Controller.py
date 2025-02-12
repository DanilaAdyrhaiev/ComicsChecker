from quart import Quart, request, jsonify
from Bot.handlers import notifyUser
from Bot.Logger import Logger

app = Quart(__name__)
logger = Logger.get_logger(__name__)
@app.route("/notify/", methods=['POST'])
async def notify():
    data = await request.get_json()
    logger.info(f"Notifying user: {data}")
    await notifyUser(data['chat_id'], data['message'])
    return jsonify({'status': 'ok'})

@app.route("/health/", methods=["GET"])
async def health_check():
    logger.info("Health check")
    return jsonify({"status": "healthy"})