#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feishu-group-welcome Skill
飞书群聊欢迎机器人
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class FeishuGroupWelcomeSkill:
    """飞书群聊欢迎技能"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.welcome_history = {}  # 记录欢迎历史，防刷屏
        
        # 配置默认值
        self.max_mentions = self.config.get("max_mentions_per_msg", 39)
        self.cooldown_minutes = self.config.get("cooldown_minutes", 10)
        self.welcome_templates = self.config.get("welcome_templates", [
            "欢迎 {mentions} 加入！🎉 我是群助手{assistant_name}～",
            "新伙伴 {mentions} 大家好！有什么问题随时问我～",
            "👋 欢迎 {mentions} 入群！一起愉快交流吧～",
            "热烈欢迎 {mentions} 加入我们的大家庭！"
        ])
        self.assistant_name = self.config.get("assistant_name", "卓然")
    
    def on_feishu_event(self, event_type: str, event_data: Dict) -> Optional[Dict]:
        """
        处理飞书事件
        """
        if event_type != "im.chat.member.user.added_v1":
            return None
        
        chat_id = event_data.get("chat_id")
        new_users = event_data.get("users", [])
        operator_id = event_data.get("operator_id")
        
        if not new_users or not chat_id:
            return None
        
        # 检查冷却时间
        if self._is_cooling_down(chat_id, new_users):
            return {"status": "cooling_down"}
        
        # 分批发送欢迎消息
        results = self._send_welcome_batches(chat_id, new_users)
        
        # 记录欢迎时间
        self._record_welcome(chat_id, new_users)
        
        return {
            "status": "success",
            "chat_id": chat_id,
            "users_welcomed": len(new_users),
            "batches_sent": len(results)
        }
    
    def _send_welcome_batches(self, chat_id: str, users: List[Dict]) -> List[Dict]:
        """
        分批发送欢迎消息（每批最多39人）
        """
        results = []
        
        # 分批处理
        for i in range(0, len(users), self.max_mentions):
            batch = users[i:i + self.max_mentions]
            
            # 构建消息
            message = self._build_welcome_message(batch)
            
            # 发送消息
            result = self._send_feishu_message(chat_id, message)
            results.append(result)
            
            # 批次间间隔，避免刷屏
            if i + self.max_mentions < len(users):
                time.sleep(1)
        
        return results
    
    def _build_welcome_message(self, users: List[Dict]) -> Dict:
        """
        构建飞书消息格式
        """
        # 生成 mentions 文本
        mentions_text = " ".join([f"@{user.get('name', '新成员')}" for user in users])
        
        # 选择欢迎语模板
        template = random.choice(self.welcome_templates)
        welcome_text = template.format(
            mentions=mentions_text,
            assistant_name=self.assistant_name,
            count=len(users)
        )
        
        # 构建飞书消息格式
        message = {
            "msg_type": "text",
            "content": {
                "text": welcome_text
            }
        }
        
        # 添加 @ 元数据
        if users:
            message["mentions"] = [
                {
                    "key": f"@{user.get('name')}",
                    "id": user.get("user_id"),
                    "name": user.get("name")
                }
                for user in users
            ]
        
        return message
    
    def _send_feishu_message(self, chat_id: str, message: Dict) -> Dict:
        """
        发送消息到飞书
        这里需要调用 OpenClaw 的飞书消息发送接口
        """
        # 实际实现需要使用 OpenClaw 的 SDK
        # 这里只是示例结构
        try:
            # 调用 OpenClaw 的飞书 API
            # from openclaw.sdk.feishu import send_message
            # response = send_message(chat_id, message)
            
            # 模拟成功返回
            return {
                "success": True,
                "chat_id": chat_id,
                "message_id": f"msg_{int(time.time())}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chat_id": chat_id
            }
    
    def _is_cooling_down(self, chat_id: str, users: List[Dict]) -> bool:
        """
        检查是否在冷却时间内
        """
        user_ids = [user.get("user_id") for user in users]
        cache_key = f"{chat_id}:{':'.join(sorted(user_ids))}"
        
        if cache_key in self.welcome_history:
            last_time = self.welcome_history[cache_key]
            cooldown_end = last_time + timedelta(minutes=self.cooldown_minutes)
            
            if datetime.now() < cooldown_end:
                return True
        
        return False
    
    def _record_welcome(self, chat_id: str, users: List[Dict]):
        """
        记录欢迎时间
        """
        user_ids = [user.get("user_id") for user in users]
        cache_key = f"{chat_id}:{':'.join(sorted(user_ids))}"
        self.welcome_history[cache_key] = datetime.now()
    
    def get_status(self) -> Dict:
        """
        获取技能状态
        """
        return {
            "name": "feishu-group-welcome",
            "enabled": True,
            "config": self.config,
            "welcome_count": len(self.welcome_history),
            "last_updated": datetime.now().isoformat()
        }


# OpenClaw 标准导出
def create_skill(config=None):
    """创建技能实例（OpenClaw 标准接口）"""
    return FeishuGroupWelcomeSkill(config)


def get_skill_info():
    """获取技能信息（OpenClaw 标准接口）"""
    return {
        "name": "feishu-group-welcome",
        "version": "1.0.0",
        "description": "飞书群聊欢迎机器人，支持批量@新成员",
        "author": "DeepWisdom",
        "event_triggers": ["im.chat.member.user.added_v1"],
        "config_schema": {
            "type": "object",
            "properties": {
                "enabled": {"type": "boolean", "default": True},
                "max_mentions_per_msg": {"type": "integer", "minimum": 1, "maximum": 39, "default": 39},
                "cooldown_minutes": {"type": "integer", "minimum": 1, "default": 10},
                "assistant_name": {"type": "string", "default": "卓然"},
                "welcome_templates": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": [
                        "欢迎 {mentions} 加入！🎉 我是群助手{assistant_name}～",
                        "新伙伴 {mentions} 大家好！有什么问题随时问我～"
                    ]
                }
            }
        }
    }
