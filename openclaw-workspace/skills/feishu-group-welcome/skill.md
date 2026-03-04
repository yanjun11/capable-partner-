# feishu-group-welcome

## 描述
飞书群聊新成员欢迎工具。当有新成员加入群聊时，自动发送欢迎消息并@所有新成员。支持批量@ - 最多39人+，分批发送避免消息过长。

## 使用场景
1. 群聊有新成员加入需要发送欢迎消息
2. 需要批量@多位新成员
3. 需要自定义欢迎语模板
4. 配置群管理助手的欢迎功能

## 功能特性
- 自动检测新成员: 通过对比群成员列表变化识别新加入的用户
- 批量@功能: 支持一次性@ 39位+新成员，分批发送（每批20人）
- 富文本@: 使用飞书 at 标签，真正的@通知而非文本@
- 多样化欢迎语: 内置6种欢迎语模板，随机选择
- 智能分批: 超过20人自动分批，第一批完整欢迎语+表情包，后续批次简化文案

## 使用方式
1. 命令行直接运行
    - 基本用法
        - 检查并欢迎所有群的新成员
          ```bash
          cd skills/feishu-group-welcome && python3 scripts/welcome_bot.py
          ```
        - 指定群聊
          ```bash
          python3 scripts/welcome_bot.py --chat-id oc_60c795e2e04eefc3d09eb49da4df15a5
          ```
        - 手动欢迎指定用户（用于补欢迎）
          ```bash
          python3 scripts/welcome_bot.py --chat-id oc_xxx --users user1,user2,user3
          ```

2. 作为群管理助手模块
    - 在 group_admin_bot.py 中导入使用:
      ```python
      from skills.feishu_group_welcome.scripts.welcome_bot import GroupWelcomeBot
      welcome_bot = GroupWelcomeBot()
      welcome_bot.check_and_welcome(chat_id, config)
      ```

3. 定时任务集成
    - 添加到 cron 定时任务，每30分钟检查一次:
      - 编辑 crontab
        ```bash
        crontab -e
        ```
      - 添加定时任务
        ```bash
        */30 * * * * cd /Users/delta/.openclaw/workspace && python3 skills/feishu-group-welcome/scripts/welcome_bot.py --chat-id oc_xxx
        ```

## 配置说明
### 环境变量
- 飞书应用凭证
  ```bash
  export FEISHU_APP_ID="cli_xxx"
  export FEISHU_APP_SECRET="xxx"
  ```

### 配置文件
- 编辑 scripts/config.py:
  ```python
  WELCOME_CONFIG = {
      "cooldown_minutes": 60,
      "batch_size": 20,
      "night_mode_start": 23,
      "night_mode_end": 7,
  }
  ```

### 欢迎语模板
- 编辑 scripts/welcome_templates.py 自定义欢迎语:
  ```python
  WELCOME_TEMPLATES = [
      "🦞 欢迎 {names} 加入「{group}」！\n\n我是卓然..."
  ]
  ```

## 注意事项
1. 飞书API限制: 只能获取当前群成员列表，无法获取历史加入记录
2. 消息撤回: 已发送的欢迎消息无法撤回，请确认后再发送
3. @上限: 飞书单条消息@人数无明确上限，但建议分批避免消息过长
4. 夜间模式: 23:00-07:00 自动静默，不发送欢迎消息

## 文件结构
```
feishu-group-welcome/
├── SKILL.md # 本文件
├── scripts/
│   ├── welcome_bot.py # 主程序
│   ├── config.py # 配置
│   ├── welcome_templates.py # 欢迎语模板
│   └── utils.py # 工具函数
└── references/
    └── api_reference.md # 飞书API参考
```

## 更新记录
- 2026-02-25: 初始版本，支持批量@和分批发送
