import jieba
import pandas as pd
from collections import Counter
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import Gauge
from pyecharts.charts import Liquid
from pyecharts.globals import SymbolType
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
from pyecharts.charts import Page


def bar_reverse():
    '''
    菜品销量排行条形图
    :return:
    '''
    x = list(df1['food_name'])
    y = list(df1['sale'])
    food_sale = list(zip(x, y))
    food_sale = sorted(food_sale, key=lambda x: x[1])
    x = [i[0] for i in food_sale]
    y = [i[1] for i in food_sale]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK,chart_id=1))
            .add_xaxis(x)
            .add_yaxis("销量", y)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="菜品销量排行"))
    )
    return c


def gauge():
    '''
    销售额仪表盘
    :return:
    '''
    df1['sale_account'] = df1['price'] * df1['sale']
    sale_account = df1['sale_account'].sum()

    c = (
        Gauge(init_opts=opts.InitOpts(theme=ThemeType.DARK,chart_id=3))
            .add(
            "业务指标",
            [("", float(sale_account))],
            split_number=5,
            detail_label_opts=opts.LabelOpts(formatter="{value}"),
            max_=100000
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="销售额完成情况",
                                      ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return c


def liquid():
    '''
    就餐人数占总作为数占比水球图
    :return:
    '''
    peo = df2.iloc[-1:, :]
    eat_peo = list(peo['eat_peo'])[0]
    seat = list(peo['seat'])[0]
    weight = round(eat_peo / seat, 2)

    c = (
        Liquid(init_opts=opts.InitOpts(theme=ThemeType.DARK,chart_id=5))
            .add("lq", [weight, weight], is_outline_show=False, shape=SymbolType.ARROW)
            .set_global_opts(title_opts=opts.TitleOpts(title="就餐人数占总座位数比重",
                                                       ))
    )
    return c


def rose():
    '''
    评分占比玫瑰图
    :return:
    '''
    score = df3['score'].value_counts()
    s = list(score.index)
    v = list(score.values)

    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK,chart_id=4))
            .add(
            "",
            [list(z) for z in zip([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])],
            radius=["30%", "75%"],
            center=["50%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="评分占比"))
    )
    return c


def wordcloud():
    '''
    评论词云图
    :return:
    '''
    comment = list(df3['comment'])
    comment = ''.join(comment).replace('\n', '')
    comment = jieba.lcut(comment)
    comment = dict(Counter(comment)).items()

    c = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.DARK,chart_id=2))
            .add(series_name="热点分析", data_pair=comment, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="评论词云",
                title_textstyle_opts=opts.TextStyleOpts(font_size=23),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return c


def bar():
    '''
    就餐人数，排队人数，剩余座位数分布柱状图
    :return:
    '''
    peo = df2.iloc[-1:, :]
    eat_peo = list(peo['eat_peo'])[0]
    queue_peo = list(peo['queue_peo'])[0]
    seat = list(peo['seat'])[0]
    odd_peo = seat - eat_peo

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK,chart_id=6))
            .add_xaxis(['用餐人数', '排队人数', '剩余座位'])
            .add_yaxis("数量", [eat_peo,queue_peo,odd_peo])
            .set_global_opts(title_opts=opts.TitleOpts(title="人数座位分布"))
    )
    return c


def page_draggable_layout():
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        bar_reverse(),
        gauge(),
        liquid(),
        rose(),
        wordcloud(),
        bar(),
    )
    page.render("page.html")
    Page.save_resize_html("page.html", cfg_file="chart_config.json", dest="my_charts.html")


if __name__ == "__main__":
    while True:
        try:
            # 读取数据
            df1 = pd.read_csv('data/food_sale.csv', encoding='utf8',engine="python")
            df2 = pd.read_csv('data/people.csv', encoding='utf8',engine="python")
            df3 = pd.read_csv('data/comment.csv', encoding='utf8',engine="python")
        except Exception as e:
            continue
        # 生成可视化仪表盘
        page_draggable_layout()

        # 插入定时刷新的代码
        with open('my_charts.html','a+') as f1:
            refesh = '<meta http-equiv="Refresh" content="3";/>  <!--页面每1秒刷新一次-->'
            f1.write(refesh)

