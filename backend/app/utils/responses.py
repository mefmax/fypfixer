from flask import jsonify

def success_response(data=None, message=None, status_code=200):
    response = {'success': True}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code

def error_response(code, message, details=None, status_code=400):
    response = {
        'success': False,
        'error': {'code': code, 'message': message}
    }
    if details:
        response['error']['details'] = details
    return jsonify(response), status_code
