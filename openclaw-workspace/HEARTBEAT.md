# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
# 飞书事件监听配置
feishu:
  events:
    member_added:
      enabled: true
      handler: welcome_new_member
      group_ids: ["oc_7725c177ac3fec7500c47047036a1b3e"]  # 你的群ID

# 欢迎处理函数
function welcome_new_member(event):
  user_name = event.user.name
  group_name = event.group.name
  
  message = f"""
👋 欢迎 {user_name} 加入 {group_name}！
  
我是本群的智能助手，很高兴为你服务。

📋 入群提示：
• 请阅读置顶消息了解群规
• 有问题随时@我
• 新人可以做个自我介绍哦～

祝你在群里交流愉快！✨
  """
  
  feishu.send_message(
    chat_id=event.chat.id,
    content=message,
    msg_type="post"  # 或 "text"、"image"等
  )
