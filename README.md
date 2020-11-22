# 1619001 收作业系统 后端
## 技术栈
Django 3.1.2 +Django Rest Framework 3.12.1
## 返回说明
本项目利用Django Rest Framework提供API，并遵循以下原则：
每个api必定返回err_code，用来标识本次操作结果，err_code不为0表示请求失败，同时返回error为错误原因，err_code=0表示请求成功，所有数据都在data里面，以下所说返回参数无特殊说明均为data里。
## 各个api说明
| API | 请求方式 | 请求参数 | 说明 |
| - | - | - |

|  API   | 请求方式 | 请求参数 | 说明 | 返回参数 | 返回类型
|  ----  | ----  | ----  | ----  | ----  | ---- |
| login | GET | 无 |检测是否登录 | done

