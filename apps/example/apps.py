from django.apps import AppConfig


class ExampleConfig(AppConfig):
    name = 'apps.example'
    verbose_name = '示例项目'


    def ready(self) -> None:
        # 加载信号
        # import apps.example.signals
        return super().ready()
    