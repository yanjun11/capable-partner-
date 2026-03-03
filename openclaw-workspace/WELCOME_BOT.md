# 欢迎机器人技能
[skill: welcome-bot]
command: /welcome
description: 新成员入群时自动发送欢迎消息
permissions: [group_admin]
trigger: feishu.member_added
actions:
  - type: feishu.send_message
    target: group
    content: |
      欢迎新成员 {user_name} 加入 {group_name}！🎉
      
      我是本群的智能助手，有什么问题随时问我～
      
      📢 群规提醒：
      1. 请修改群昵称为真实姓名
      2. 禁止发布广告
      3. 友好交流，互相帮助
      
      点击查看完整群规：{group_rules_url}
    buttons:
      - text: "查看帮助文档"
        url: "https://docs.example.com"
      - text: "联系管理员"
        url: "feishu://contact/admin"
