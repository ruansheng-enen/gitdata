#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/6/13 14:15
@Author  : hqy
@Version : 1.0
@Modify Time : 2023/6/13 14:15
@Description : 
轻量级异步接口demo，通过异步线程实现
"""
import os
import sys
import json
import re
import time
from flask_restful import Resource, Api, reqparse, abort
from flask import request,Flask,jsonify, make_response

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)

# 异常参数代码
resultcode_map = {
    "AI_200": "操作成功",
    "AI_500": "操作失败",
    "AI_400": "请求无法解析（参数错误、协议错误等）",
    # 参数错误，允许启用参数默认值，
    "AI_201": "操作成功，**参数为空，已启用默认值**",
    "AI_202": "操作成功，**参数为无效值，已启用默认值**",
    # 请求方式错误
    "AI_401": "请求方式错误！",
    # 参数错误，导致操作终止
    "AI_405": "参数为空，**参数不能为空!",
    # 文件类参数
    "AI_415": "文件类型不支持!当前仅支持doc/docx/txt/pdf",
    "AI_416": "文件大小不符合!当前支持范围10M以内",
    # 文件类
    "AI_503": "文件不存在",
    "AI_506": "文件读取失败",
    "AI_508": "文件写入保存失败",
    # 类型转换
    "AI_513": "文本向量化失败",
    "AI_515": "文本转Document类型失败",
    "AI_522": "文本prompt化失败",
    # 使用本地模型
    "AI_531": "模型不存在",
    "AI_532": "模型运行异常",
    "AI_540":"LLM接口不可达"
}

class asyncFun(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=list, location='json')
        parser.add_argument('maxNums', type=str, location='json')
        args = parser.parse_args()
        # 参数有效性校验

        # 线程传参要求dict类型
        args_dict = {
            "fileID": args["fileID"],
            "maxNums": args["maxNums"]
        }

        # 交由线程去执行耗时任务
        executor.submit(self.do_blocking_work, args_dict)

        print("get the request success")
        # 写入redis ，taskID的任务请求已收到

        result_data = {
            "code": "200",
            "msg": "操作成功",
            "resultCode": "",
            "success": True,
        }
        return result_data

    def do_blocking_work(self, args_dict):
        time.sleep(10)
        print(args_dict)
        # 写入redis 编号为taskID的任务已完成
        print("Finished work {taskID}")
        print('a')

def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app, default_mediatype="application/json")

    api.add_resource(asyncFun, '/ylkj-nlp/gpt-app-documents/get-fun')

    return app

    