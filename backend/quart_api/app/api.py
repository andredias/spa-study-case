from quart import Blueprint

api = Blueprint('api', __name__)


@api.route('/hello')
async def hello():
    return {'hello': 'world'}
