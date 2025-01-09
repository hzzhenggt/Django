# 简介
此模板介绍如何将 Django 与 Python 一起使用。
# 开始
* 单击 **运行** 按钮启动程序。
![图片](https://lf-cdn.marscode.com.cn/obj/eden-cn/ljhwz_lkpkbvsj/ljhwZthlaukjlkulzlp/project_template/prod/6a7bb0d45e3826780749b19626dc67986c720e60/images/native_python_django/image-0.jpg)

* 转到 端口 并预览页面 **端口：8080。**

   ![图片](https://lf-cdn.marscode.com.cn/obj/eden-cn/ljhwz_lkpkbvsj/ljhwZthlaukjlkulzlp/project_template/prod/6a7bb0d45e3826780749b19626dc67986c720e60/images/native_python_django/cloud_port.jpeg)

* 转到 Webview 查看实时页面。

   ![图片](https://lf-cdn.marscode.com.cn/obj/eden-cn/ljhwz_lkpkbvsj/ljhwZthlaukjlkulzlp/project_template/prod/6a7bb0d45e3826780749b19626dc67986c720e60/images/native_python_django/preview.jpeg)

默认情况下，MarsCode运行 **manage.py**，你可以更改 **. vscode/launch.json** 中的配置。参考 [Visual Studio Code的文档](https://code.visualstudio.com/docs/editor/debugging) 有关如何配置launch. json。
# 了解更多
- [Python](https://www.python.org/) -Python编程语言的官方主页。
- [Django](https://www.djangoproject.com/) -了解Django功能。
# 帮助
如果你需要帮助，你可以查看[文档](https://docs.marscode.cn/)，或向我们提供[反馈](https://juejin.cn/pin/club/7359094304150650889?utm_source=doc&utm_medium=marscode)。

# 需求设计
```
# Django项目架构

## 1. 项目基础
### 1.1 项目结构
- django_app/
  - settings.py (项目配置)
  - urls.py (URL路由)
- apps/
  - core/ (核心功能)
  - example/ (示例应用)
- docs/ (文档)
- requirements.txt (依赖)
- manage.py (管理脚本)

### 1.2 基础配置
- 数据库配置
- 中间件配置
- 应用注册
- 静态文件配置

## 2. 核心功能 (core)
### 2.1 基础模型
- BaseModel
  - id默认主键
  - 创建时间
  - 更新时间
  - 软删除标记
  - sort排序

### 2.2 视图层
- BaseView
  - 权限控制
  - 异常处理
  - 响应格式化
- CRUDView
  - 列表查询
  - 详情查询
  - 创建
  - 更新
  - 删除

### 2.3 工具类
- 数据验证
- 缓存处理
- 分页
- 过滤和搜索

## 3. 示例应用 (example)
### 3.1 业务模型
- Project (项目)
- Task (任务)

### 3.2 API实现
- 项目管理
- 任务管理

### 3.3 测试用例
- 单元测试
- 集成测试
```