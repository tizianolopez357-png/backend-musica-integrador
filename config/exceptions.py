from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    if isinstance(response.data, dict) and 'detail' in response.data:
        detail = response.data['detail']
        response.data = {'detail': str(detail)}
    else:
        response.data = {
            'detail': 'Error en la solicitud.',
            'errors': response.data,
        }
    return response
