# coding=utf-8
'''aliyun mns'''

# import json
# from functools import wraps

# from flask import make_response, request

# from .LogHelper import CLogHelper
# from .utils import format_exception

# # 日志输出对象
# log = CLogHelper.logger


# def mns_request_auth(request):
#     '''
#     对MNS的订阅消息进行验证

#     args:
#         request: flask.request对象

#     return:
#         bool.
#     '''
#     import base64
#     import urllib2
#     import M2Crypto

#     headers = {}
#     # if isinstance(req.headers, (werkzeug.datastructures.EnvironHeaders)):
#     for k in request.headers:
#         headers[k[0]] = k[1].encode('utf-8')

#     service_str = "\n".join(
#         sorted([
#             "%s:%s" % (k.lower(), v) for k, v in headers.items()
#             if k.lower().startswith("x-mns-")
#         ]))
#     sign_header_list = []
#     for key in ["Content-Md5", "Content-Type", "Date"]:
#         if key in headers.keys():
#             sign_header_list.append(headers[key])
#         else:
#             sign_header_list.append("")
#     str2sign = "%s\n%s\n%s\n%s" % (request.method, "\n".join(sign_header_list),
#                                    service_str, request.path)
#     str2sign = str2sign.encode('utf-8')

#     authorization = headers['Authorization']
#     signature = base64.b64decode(authorization)
#     cert_str = urllib2.urlopen(
#         base64.b64decode(headers['X-Mns-Signing-Cert-Url'])).read()
#     pubkey = M2Crypto.X509.load_cert_string(cert_str).get_pubkey()
#     pubkey.reset_context(md='sha1')
#     pubkey.verify_init()
#     pubkey.verify_update(str2sign)
#     r = pubkey.verify_final(signature)
#     return r


# def mns_request_decorator(fn):
#     ''' mns推送请求处理装饰器 '''

#     @wraps(fn)
#     def __wrapper(*arg, **kw):
#         '''
#         统一处理MNS的推送请求

#         return:
#             204, 500
#         '''
#         try:
#             args = json.loads(request.get_data())
#             log.sequence_id = args['meta']['sequence_id']
#             args['meta']['mns_message_id'] = request.headers[
#                 'x-mns-message-id']
#             fn(args, *arg, **kw)
#             return make_response('', 204)
#         except Exception as ex:
#             log.critical(format_exception(ex))
#             return make_response('', 500)

#     return __wrapper
