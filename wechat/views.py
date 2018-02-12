#-*- coding: utf8 -*-
import hashlib, time
import xml.etree.ElementTree as ET

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str

from utility.transtool import Transfer


def checkSignature(request):
    '''Check the signature from wechat api for the first bind'''
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr  = request.GET.get('echostr', None)

    token = 'jaydenzheteng'

    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = '%s%s%s'%tuple(tmplist)
    tmpstr = hashlib.sha1(tmpstr.encode('utf-8')).hexdigest()
    if tmpstr == signature:
        return echostr
    else:
        return None

def parseMsgXml(rootElem):
    '''Parse the xml response get from wechat api'''
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg

def getReplyXml(msg,replyContent):
    '''Create the xml response content for wechat api'''
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
    extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text', replyContent)
    return extTpl

@csrf_exempt
def WechatIndexView(request):
    '''Main view function for wechat'''
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request))
        return response
    else:
        rawStr = smart_str(request.body)
        msg = parseMsgXml(ET.fromstring(rawStr))
        queryStr = msg.get('Content', 'You have input nothing')

        # queryStr = request.POST['str']
        trans = Transfer()
        res = trans.transfer(queryStr)
        return HttpResponse(getReplyXml(msg, res), content_type='text/xml')

def WechatTestView(request):
    '''Just for test'''
    return render(request, 'wechat/wechat_transfer_test.html')
