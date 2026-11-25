# 长剧追更曲线与断档编排

不同地区会员的追更观察和回归排期。片段范围以秒计，许可日期以当地业务日计。合并版 M 载有两个可分别完成的片段。观察期资料包含落在窗口末日的播放。 各表日期起止均含当日。数据切点表同时区分观察时点和资料收齐日。已观察的播放保留源事实，是否计作有效续看以会员期和许可窗口为准。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- episodes.csv 的字段为 edition、segment、story_episode、begin、end、min_complete_seconds。
- windows.csv 的字段为 window、region、tier、story_episode、start、stop、revision。
- memberships.csv 的字段为 household、region、tier、start、stop。
- views.csv 的字段为 view、household、edition、segment、started_on、begin、end。
- promises.csv 的字段为 notice、household、window、public_date、promised_day、state。
- returns.csv 的字段为 plan、region、edition、release_day、translation_job、provider、capacity_units、available_units。
- observation.csv 的字段为 cut、as_of、data_received、license_rev。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
