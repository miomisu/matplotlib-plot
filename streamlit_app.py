import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.font_manager import FontProperties

st.set_page_config(
    page_title="matplotlib GUI",
    page_icon="📈"
)

st.title("matplotlibで散布図を作成")

tab1, tab2, tab3, tab4 = st.tabs(["基本のプロット", "高度な設定", "使い方", "既知の不具合"])

# ファイル読み込み用関数
@st.cache_data
def get_data(file):# -> np.ndarray:
    data_set = np.genfromtxt(
        fname=file,
        dtype="float",
        delimiter=dlmt,
        skip_header=sh,
    )
    return data_set

@st.cache_data
def get_data2(file) -> np.ndarray:
    data_set = np.genfromtxt(
        fname=file,
        dtype="float",
        delimiter=dlmt,
        skip_header=sh,
    )
    return data_set

# クラス作成
class plot_main:
    def __init__(self, dpi, width, height, toptick, bottomtick, lefttick, righttick, xtickdir, ytickdir, property, legends, ja_legends, minorticks, grid, xlog, ylog, xmin, xmax, ymin, ymax, xscale, yscale, fontsize, xlabel, ylabel, fp, column, xaxis, xtick_list_num, xtick_list, ytick_list_num, ytick_list, ticksetting, xmajor_size, ymajor_size, xminor_size, yminor_size, xmajor_width, ymajor_width, xminor_width, yminor_width, title, expantion):
        self.dpi = dpi
        self.width = width
        self.height = height
        self.toptick = toptick
        self.bottomtick = bottomtick
        self.lefttick = lefttick
        self.righttick = righttick
        self.xtickdir = xtickdir
        self.ytickdir = ytickdir
        self.property = property
        self.legends = legends
        self.ja_legends = ja_legends
        self.minorticks = minorticks
        self.grid = grid
        self.xlog = xlog
        self.ylog = ylog
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.xscale = xscale
        self.yscale = yscale
        self.fontsize = fontsize
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.fp = fp
        self.column = column
        self.xaxis = xaxis
        self.xtick_list_num = xtick_list_num
        self.xtick_list = xtick_list
        self.ytick_list_num = ytick_list_num
        self.ytick_list = ytick_list
        self.ticksetting = ticksetting
        self.xmajor_size = xmajor_size
        self.ymajor_size = ymajor_size
        self.xminor_size = xminor_size
        self.yminor_size = yminor_size
        self.xmajor_width = xmajor_width
        self.ymajor_width = ymajor_width
        self.xminor_width = xminor_width
        self.yminor_width = yminor_width
        self.title = title
        self.expantion = expantion
    
    # figure作成
    def makefig(self):
        fig = plt.figure(dpi=self.dpi, figsize=(self.width, self.height))
        return fig
    
    # 目盛り有無
    def enable_ticks(self):
        plt.rcParams["xtick.top"] = self.toptick
        plt.rcParams["xtick.bottom"] = self.bottomtick
        plt.rcParams["ytick.left"] = self.lefttick
        plt.rcParams["ytick.right"] = self.righttick
    
    # 目盛り向き
    def tick_direction(self):
        if self.xtickdir == "内側":
            plt.rcParams["xtick.direction"] = "in"
        elif self.xtickdir == "外側":
            plt.rcParams["xtick.direction"] = "out"
        else:
            plt.rcParams["xtick.direction"] = "inout"

        if self.ytickdir == "内側":
            plt.rcParams["ytick.direction"] = "in"
        elif self.ytickdir == "外側":
            plt.rcParams["ytick.direction"] = "out"
        else:
            plt.rcParams["ytick.direction"] = "inout"
    
    # 目盛り線
    def custom_ticks(self):
        if self.ticksetting:
            plt.rcParams["xtick.major.size"] = self.xmajor_size
            plt.rcParams["ytick.major.size"] = self.ymajor_size
            plt.rcParams["xtick.minor.size"] = self.xminor_size
            plt.rcParams["ytick.minor.size"] = self.yminor_size
            plt.rcParams["xtick.major.width"] = self.xmajor_width
            plt.rcParams["ytick.major.width"] = self.ymajor_width
            plt.rcParams["xtick.minor.width"] = self.xminor_width
            plt.rcParams["ytick.minor.width"] = self.yminor_width
        else:
            plt.rcParams["xtick.major.size"] = 4.0
            plt.rcParams["ytick.major.size"] = 4.0
            plt.rcParams["xtick.minor.size"] = 2.0
            plt.rcParams["ytick.minor.size"] = 2.0
            plt.rcParams["xtick.major.width"] = 1.0
            plt.rcParams["ytick.major.width"] = 1.0
            plt.rcParams["xtick.minor.width"] = 0.6
            plt.rcParams["ytick.minor.width"] = 0.6
            
    def valueplot(self):
        for o in self.property:
            if any(np.isnan(self.column[o[0]])):
                    st.write("第" + str(o[0]) + "列に欠損値があるため折れ線を表示できません。")
                    plt.scatter(self.column[self.xaxis], self.column[o[0]], marker=o[1][0], s=o[2], c=o[4], label=o[5])
            else:
                plt.plot(self.column[self.xaxis], self.column[o[0]], o[1], markersize=o[2], linewidth=o[3], c=o[4], label=o[5])
    
    # 凡例表示
    def display_legend(self):
        if self.legends == True and self.ja_legends == False:
            plt.legend(fontsize = self.fontsize)
        if self.legends == True and self.ja_legends == True:
            plt.legend(fontsize = self.fontsize, prop={"family":"Meiryo"})
    
    # 副目盛り追加
    def add_minorticks(self):
        if self.minorticks:
            plt.minorticks_on()
    
    # グリッド表示
    def display_grid(self):
        if self.grid:
            plt.grid()

    # x軸対数指定
    def enable_xlog(self):
        if self.xlog:
            plt.xscale("log")
    # y軸対数指定
    def enable_ylog(self):
        if self.ylog:
            plt.yscale("log")
    
    # x軸範囲
    def xrange(self):
        if self.xmin != None and self.xmax != None:
            plt.xlim(self.xmin, self.xmax)
    # y軸範囲
    def yrange(self):
        if self.ymin != None and self.ymax != None:
            plt.ylim(self.ymin, self.ymax)
    
    # 軸目盛り
    def set_ticks(self):
        if self.xscale:
            plt.xticks(self.xtick_list_num, self.xtick_list, fontsize = self.fontsize)
        else:
            plt.xticks(fontsize = self.fontsize)
        if self.yscale:
            plt.yticks(self.ytick_list_num, self.ytick_list, fontsize = self.fontsize)
        else:
            plt.yticks(fontsize = self.fontsize)
    
    # X軸ラベル
    def add_xlabel(self):
        plt.xlabel(self.xlabel, fontproperties = self.fp)
    # Y軸ラベル
    def add_ylabel(self):
        plt.ylabel(self.ylabel, fontproperties=self.fp)

    # プロット(完全)
    def plot_fig(self) -> matplotlib.figure.Figure:
        fig = self.makefig(self.dpi, self.width, self.height)
        self.enable_ticks(self.toptick, self.bottomtick, self.lefttick, self.righttick)
        self.tick_direction(self.xtickdir, self.ytickdir)
        self.custom_ticks(self.ticksetting, self.xmajor_size, self.ymajor_size, self.xminor_size, self.yminor_size, self.xmajor_width, self.ymajor_width, self.xminor_width, self.yminor_width)
        self.valueplot(self.property, self.column)
        self.display_legend(self.legends, self.ja_legends, self.fontsize)
        self.add_minorticks(self.minorticks)
        self.display_grid(self.grid)
        self.enable_xlog(self.xlog)
        self.enable_ylog(self.ylog)
        self.xrange(self.xmin, self.xmax)
        self.yrange(self.ymin, self.ymax)
        self.set_ticks(self.xscale, self.xtick_list_num, self.xtick_list, self.yscale, self.ytick_list_num, self.ytick_list, self.fontsize)
        self.add_xlabel(self.xlabel, self.fp)
        self.add_ylabel(self.ylabel, self.fp)
        return fig
    
    # プロット(凡例なし)
    def plot_fig_nolegend(self) -> matplotlib.figure.Figure:
        fig = self.makefig(self.dpi, self.width, self.height)
        self.enable_ticks(self.toptick, self.bottomtick, self.lefttick, self.righttick)
        self.tick_direction(self.xtickdir, self.ytickdir)
        self.custom_ticks(self.ticksetting, self.xmajor_size, self.ymajor_size, self.xminor_size, self.yminor_size, self.xmajor_width, self.ymajor_width, self.xminor_width, self.yminor_width)
        self.valueplot(self.property, self.column)
        self.add_minorticks(self.minorticks)
        self.display_grid(self.grid)
        self.enable_xlog(self.xlog)
        self.enable_ylog(self.ylog)
        self.xrange(self.xmin, self.xmax)
        self.yrange(self.ymin, self.ymax)
        self.set_ticks(self.xscale, self.xtick_list_num, self.xtick_list, self.yscale, self.ytick_list_num, self.ytick_list, self.fontsize)
        self.add_xlabel(self.xlabel, self.fp)
        self.add_ylabel(self.ylabel, self.fp)
        return fig

# マーカーのオプション
colors = ["white", "black", "gray", "lightgrey", "red", "coral", "orangered", "sandybrown", "darkorange", "orange", "gold", "yellow", "lawngreen", "green", "darkgreen", "lime", "aqua", "dodgerblue", "royalblue", "darkblue", "violet", "purple", "magenta", "hotpink"]
markers_dict = {"●": "o", "■": ",", "▼": "v", "▲": "^","◆": "D", "✚": "+", "✖": "x"}
linetype_dict = {"実線":"-", "破線":"--", "点線":":", "一点鎖線":"-."}

# オブジェクト作成
param_list = [None for i in range(43)]
a = plot_main(*param_list)

with tab1:
    with st.sidebar:
        st.subheader("基本設定")
        # ファイル読み込みオプション
        sh = st.number_input("無視する先頭からの行数", min_value=0, max_value=50, value="min", step=1)
        ft = st.radio("ファイルの種類", ["CSV(カンマ区切り)", "TSV(タブ区切り)"])
        if ft == "CSV(カンマ区切り)":
            dlmt = ","
        else:
            dlmt = "\t"
        # ファイル読み込み
        st.subheader("ファイルを選択")
        uploaded_file = st.file_uploader("数値だけが入力されたCSV、TSV、TXTファイルを選択", type=["csv", "tsv", "txt"])

        if uploaded_file:
            data_set = get_data(uploaded_file)
            with st.expander("データを見る"):
                st.write(data_set)

        # グラフのオプション
        st.subheader("グラフのオプション")
        col1, col2 = st.columns(2)
        with col1:
            a.xmin = st.number_input("X軸の最小値", value=None, step=0.1)
        with col2:
            a.xmax = st.number_input("X軸の最大値", value=None, step=0.1)
        st.caption("両方とも入力していない場合自動で調整されます")
        st.caption("0.01未満の値を入力した場合0.00と表示されます")
        if a.xmin != None:
            if a.xmax != None:
                if a.xmin > a.xmax:
                    st.error("最小値が最大値より大きくなっています", icon="🚨")

        col1, col2 = st.columns(2)
        with col1:
            a.ymin = st.number_input("Y軸の最小値", value=None, step=0.01)

        with col2:
            a.ymax = st.number_input("Y軸の最大値", value=None, step=0.01)
        st.caption("両方とも入力していない場合自動で調整されます")
        st.caption("0.01未満の値を入力した場合0.00と表示されます")
        if a.ymin != None:
            if a.ymax != None:
                if a.ymin > a.ymax:
                    st.error("最小値が最大値より大きくなっています", icon="🚨")

        with st.expander("目盛りの詳細設定"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                a.toptick = st.checkbox("上側目盛り", value=False)
            with col2:
                a.bottomtick = st.checkbox("下側目盛り", value=True)
            with col3:
                a.lefttick = st.checkbox("左側目盛り", value=True)
            with col4:
                a.righttick = st.checkbox("右側目盛り", value=False)

            col1, col2 = st.columns(2)
            with col1:
                a.xtickdir = st.radio("X軸の目盛りの向き", ["内側", "外側", "両方"], horizontal=True, index=0)
            with col2:
                a.ytickdir = st.radio("Y軸の目盛りの向き", ["内側", "外側", "両方"], horizontal=True, index=0)

            a.xscale = st.checkbox("X軸の目盛りの位置を設定", value = False)
            xtick = st.text_input("目盛りを表示する位置(数値)をスペースで区切って入力", key = "xtick")
            a.xtick_list = xtick.split()
            try:
                a.xtick_list_num = [float(i) for i in a.xtick_list]
            except:
                st.error("数値を入力してください", icon="🚨")

            a.yscale = st.checkbox("Y軸の目盛りの位置を設定", value = False)
            ytick = st.text_input("目盛りを表示する位置(数値)をスペースで区切って入力", key = "ytick")
            a.ytick_list = ytick.split()
            try:
                a.ytick_list_num = [float(i) for i in a.ytick_list]
            except:
                st.error("数値を入力してください", icon="🚨")

            a.minorticks = st.checkbox("副目盛り", value="True")

        col1, col2 = st.columns(2)
        with col1:
            a.xlabel = st.text_input("X軸のラベル", "X")
        with col2:
            a.ylabel = st.text_input("Y軸のラベル", "Y")
        st.caption("$で囲むことでTeX記法の数式を使用可能")

        col1, col2 = st.columns(2)
        with col1:
            a.xlog = st.checkbox("X軸を対数軸にする", value=False)
            a.legends = st.checkbox("凡例表示", value=False)
            a.ja_legends = False
            if a.legends:
                a.ja_legends = st.checkbox("凡例名に日本語を用いる", value = False, disabled=True)
            # フォント指定
            a.fontsize = st.number_input("フォントサイズ", step=1, value=12)
            a.fp = FontProperties(fname=r"NotoSansJP-Regular.ttf", size=a.fontsize)

        with col2:
            a.ylog = st.checkbox("Y軸を対数軸にする", value=False)
            a.grid = st.checkbox("グリッド", value="True")



        if uploaded_file:
            #data_set = get_data(uploaded_file)
            # st.write(uploaded_file.name)
            columns = []
            # 行列入れ替え
            try:
                a.column = [[] for i in range(len(data_set[0]))]
                for i in range(len(data_set[0])):
                    columns.append(i)
                    for j in range(len(data_set)):
                        a.column[i].append(data_set[j][i])
            except:
                st.error("正しいファイルを選択できているか確認してください", icon="🚨")

            # st.write(data_set[0])
            # st.write(type(data_set))

            col1, col2 = st.columns(2)
            with col1:
                a.xaxis = st.selectbox("Xとする列", columns)
            with col2:
                yaxis = st.multiselect("Yとする列（複数選択可）", columns)
            if a.xaxis in yaxis:
                st.error("X軸とY軸で同じ列を選択しています", icon="🚨")

            # プロットオプション
            #if yaxis != None:
            if a.xaxis not in yaxis:
                if yaxis:
                    st.write("マーカーのオプション")
                a.property = [[] for i in range(len(yaxis))]
                for i, ycolumn in enumerate(yaxis):
                    a.property[i].append(ycolumn)
                    st.write("第" + str(ycolumn) + "列")
                    plottype = st.radio("プロットの種類", ["マーカー", "折れ線", "両方"], horizontal=True, key=i + 0.5, disabled=any(np.isnan(a.column[ycolumn])))
                    col1, col2, col3= st.columns(3)
                    with col1:
                        marker = st.selectbox("マーカーの形", (markers_dict.keys()), key = i + 0.1)
                        linetype = st.selectbox("線の種類", (linetype_dict.keys()), key=i + 0.6)
                        if plottype == "マーカー":
                            a.property[i].append(markers_dict[marker])
                        elif plottype == "折れ線":
                            a.property[i].append(linetype_dict[linetype])
                        elif plottype == "両方":
                            a.property[i].append(markers_dict[marker] + linetype_dict[linetype])
                    with col2:
                        markersize = st.number_input("マーカーの大きさ", value = 4, min_value = 0, step = 1, key = i + 0.2)
                        a.property[i].append(markersize)
                        linewidth = st.number_input("線の幅", value = 3, min_value = 0, step = 1, key = i + 0.7)
                        a.property[i].append(linewidth)
                    with col3:
                        color = st.selectbox("色", (colors), key = i, index=1)
                        a.property[i].append(color)
                        legend = st.text_input("凡例名", key = i + 0.3)
                        a.property[i].append(legend)
                #st.write(property)
            st.write("グラフのサイズ")
            col1, col2, col3= st.columns(3)
            with col1:
                a.dpi = st.number_input("dpi", value = 300, step = 1, min_value = 10)
            with col2:
                a.width = st.number_input("幅(インチ)", value = 8, step = 1, min_value = 1)
            with col3:
                a.height = st.number_input("高さ(インチ)", value = 6, step = 1, min_value = 1)
            st.write("サイズ(余白削除前)  :    " + str(a.width * a.dpi) + "×" + str(a.height * a.dpi))

            col1, col2 = st.columns(2)
            with col1:
                a.title = st.text_input("保存するファイル名", "plot")
            with col2:
                a.expantion = st.selectbox("保存する拡張子", (".png", ".jpg", ".svg", ".pdf"))
            st.caption("svg, pdfの場合プロットする点が多いと保存した画像が重くなるので注意")

    st.write("←サイドバーを開いて設定を表示(サイズ変更可能)")
    if uploaded_file:
        # プロット
        # fig = a.plot_fig() <-エラーが出る
        fig = a.makefig()
        plt.rcParams["grid.linewidth"] = 0.8
        plt.rcParams["axes.linewidth"] = 0.8
        plt.rcParams["grid.color"] = "#b0b0b0"
        a.enable_ticks()
        a.tick_direction()
        a.custom_ticks()
        a.valueplot()
        a.display_legend()
        a.add_minorticks()
        a.display_grid()
        a.enable_xlog()
        a.enable_ylog()
        a.xrange()
        a.yrange()
        a.set_ticks()
        a.add_xlabel()
        a.add_ylabel()
        # 表示
        st.pyplot(fig)
        # 保存
        plt.savefig(a.title + a.expantion, bbox_inches="tight")
        # ダウンロード
        with open(a.title + a.expantion, "rb") as file:
            btn = st.download_button(
                label = "画像を保存",
                data = file,
                file_name = a.title + a.expantion,
                )


with tab2:
    st.subheader("高度な設定")
    with st.expander("ユーザー関数を表示"):
        function = st.checkbox("有効化", value = False, key="function")
        f = st.text_input("表示したいxの関数を入力", placeholder = "例) np.sin(x), x**2 - 4*x + 3")
        st.caption("累乗はアスタリスク2つ(**)で表す 三角関数等はhttps://deepage.net/features/numpy-math.html などを参照")
        st.write("表示する範囲(入力必須)")
        # オプション
        col1, col2, col3 = st.columns(3)
        with col1:
            f_min = st.number_input("最小値", value=0.0, step=0.01)
        with col2:
            f_max = st.number_input("最大値", value=10.0, step=0.01)
        with col3:
            slice = st.number_input("分割数(滑らかさ)", value = 100, min_value = 0, step = 1)

        st.write("オプション")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            f_linetype = st.selectbox("線の種類", (linetype_dict.keys()))
        with col2:
            f_color = st.selectbox("色", (colors), index=1)
        with col3:
            f_size = st.number_input("線の幅", value = 3.0, min_value = 0.0, step = 0.5)
        with col4:
            f_legend = st.text_input("凡例名")
        
        if f_max <= f_min:
            st.error("最小値が最大値よりも大きくなっています", icon="🚨")
        else:
            try:
                x = np.linspace(f_min, f_max, slice)
            except:
                st.error("範囲を正しく入力できているか確認してください", icon="🚨")
        y = []
        
        # 配列作成
        if f and f_max > f_min:
            try:
                for i in x:
                    y = eval(f)
            except:
                st.error("関数を正しく入力できているか確認してください", icon="🚨")

    with st.expander("フォントを指定する(軸ラベルのみ)"):
        setfont = st.checkbox("有効化", value = False, disabled=True, key="font")
        fontpath = st.text_input("フォントファイルのパスを指定", placeholder = "例) C:\Windows\Fonts\HGRPP1.ttc")
        if fontpath:
            fp = FontProperties(fname=fontpath, size=a.fontsize)
        st.caption("システムフォントの場所 C:\\Windows\\Fonts ユーザーフォントの場所 C:\\Users\\ユーザー名\\AppData\\Local\\Microsoft\\Windows\\Fonts")
    
    with st.expander("目盛り線の設定"):
        a.ticksetting = st.checkbox("有効化", value=False, key="ticksetting")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            a.xmajor_size = st.number_input("X軸主目盛り線長さ", value=4.0, step=0.1, min_value=0.0)
            a.ymajor_size = st.number_input("Y軸主目盛り線長さ", value=4.0, step=0.1, min_value=0.0)
        with col2:
            a.xminor_size = st.number_input("X軸副目盛り線長さ", value=2.0, step=0.1, min_value=0.0)
            a.yminor_size = st.number_input("Y軸副目盛り線長さ", value=2.0, step=0.1, min_value=0.0)
        with col3:
            a.xmajor_width = st.number_input("X軸主目盛り線幅", value=1.0, step=0.1, min_value=0.0)
            a.ymajor_width = st.number_input("Y軸主目盛り線幅", value=1.0, step=0.1, min_value=0.0)
        with col4:
            a.xminor_width = st.number_input("X軸副目盛り線幅", value=0.6, step=0.1, min_value=0.0)
            a.yminor_width = st.number_input("Y軸副目盛り線幅", value=0.6, step=0.1, min_value=0.0)

    with st.expander("凡例の詳細設定"):
        legendsetting = st.checkbox("有効化", value=False, key="legendsetting")
        col1, col2 = st.columns(2)
        with col1:
            legend_frame = st.checkbox("枠を表示", value=True)
            legend_transparency = st.slider("背景の不透明度", min_value=0.0, max_value=1.0, step=0.1, value=0.8)
        with col2:
            legend_corner = st.checkbox("角を丸める", value=True)
            legend_cols = st.slider("凡例の列数", min_value=1, max_value=5, step=1)
        col1, col2, col3 = st.columns(3)
        with col1:
            legend_framecolor = st.selectbox("枠の色", (colors), index=1)
        with col2:
            legend_color = st.selectbox("背景の色", (colors))
        with col3:
            legend_lettercolor = st.selectbox("文字の色", (colors), index=1)

    with st.expander("その他の設定"):
        col1, col2, col3 = st.columns(3)
        with col1:
            setframewidh = st.checkbox("グラフの枠の幅を設定", value=False)
            framewidth = st.number_input("グラフの枠の幅", value=0.8, min_value=0.0, step=0.1, disabled=not setframewidh)
        with col2:
            setgridwidth =  st.checkbox("グリッドの線幅を設定", value=False)
            gridwidth = st.number_input("グリッドの線幅", value=0.8, min_value=0.0, step=0.1, disabled=not setgridwidth)
        with col3:
            setgridcolor = st.checkbox("グリッドの色を選択", value=False)
            gridcolor = st.selectbox("色を選択", (colors), key="gridcolor", disabled=not setgridcolor, index=3)

    if function or setfont or a.ticksetting or setframewidh or setgridwidth or setgridcolor or legendsetting:
        if uploaded_file:
            adv_fig = a.makefig()
            # 設定適用
            if function and f and f_max > f_min:
                plt.plot(x, y, linetype_dict[f_linetype], c = f_color, linewidth = f_size, label = f_legend)
            if setgridwidth:
                plt.rcParams["grid.linewidth"] = gridwidth
            if setframewidh:
                plt.rcParams["axes.linewidth"] = framewidth
            if setgridcolor:
                plt.rcParams["grid.color"] = gridcolor

            a.enable_ticks()
            a.tick_direction()
            a.custom_ticks()
            a.valueplot()
            if legendsetting:
                plt.legend(fontsize=a.fontsize, frameon=legend_frame, fancybox=legend_corner, facecolor=legend_color, framealpha=legend_transparency, edgecolor=legend_framecolor, ncol=legend_cols, labelcolor=legend_lettercolor)
            else:
                a.display_legend()
            a.add_minorticks()
            a.display_grid()
            a.enable_xlog()
            a.enable_ylog()
            a.xrange()
            a.yrange()
            a.set_ticks()
            a.add_xlabel()
            a.add_ylabel()
            try:
                st.pyplot(adv_fig)
                # 保存
                plt.savefig(a.title + a.expantion, bbox_inches="tight")
                # ダウンロード
                with open(a.title + a.expantion, "rb") as file:
                    btn = st.download_button(
                        label = "画像を保存",
                        data = file,
                        file_name = a.title + a.expantion,
                        key="adv_download"
                        )
            except:
                st.error("フォントファイルのパスを正しく入力できているか確認してください", icon="🚨")
    

with tab3:
    st.subheader("基本の使い方")
    '''
    1. プロットしたいデータのファイルを用意する
        - カンマ区切り(csv)、タブ区切り(tsv)の形式のファイルを使用可能
        - 数値データのみが含まれるようにする
        - エクセルでプロットしたい範囲のデータをコピーし、空のテキストファイルに貼り付けて保存することでtsv形式として保存可能
    2. ファイルを読み込む
        - タイトル行などがある場合はその行数を入力する
        - ファイルの種類を選択する
        - ファイルをドラッグアンドドロップ、または「Browse files」をクリックしてファイルを選択する
        - 「データを見る」を開くことで読み込んだデータを確認可能
    3. オプションを選択する
        - グラフのX軸、Y軸の範囲を選択する 入力しない場合、自動で調整される
        - 「目盛りの詳細設定」で目盛りの表示/非表示や向き、主目盛りの位置を設定可能
        - 軸のラベルを入力する $で囲むことでTeX記法の数式を使用可能
        - :orange[日本語の凡例名表示は未対応]
    4. プロットするデータを選択する
        - X、Yとするデータの列を選択する Yとするデータの列は複数選択可能
        - 列を選択するとそのデータの表示設定が表示されるので変更する
        - 折れ線グラフも追加可能 ただしデータに欠損値が存在する場合は未対応
    5. 保存する画像の設定を変更する
        - dpi=1インチあたりのドット数
        - ベクター形式のpdf、svgで保存すると拡大しても粗くならないが、プロットする点が極端に多い場合保存した画像の読み込みなどが重くなることがあるので注意
    6. 画像を保存する
        - 設定を変更して完成したら「画像を保存」ボタンを押して画像をダウンロードできる
    '''
    st.subheader("高度な設定")
    '''
    - 関数を表示
        - 散布図に関数のグラフを表示可能
        - xを変数とした関数を入力する
        - 一般的な数式のように四則演算を入力可能 足し算:`+` 引き算:`-`  掛け算`*` 割り算:`/` 累乗:`**`
        - 三角関数や対数関数はnumpyというライブラリの表記に従って入力する
    - フォントの指定
        - サーバー上での動作では未対応
    - 目盛り線の設定
        - 各軸の主、副目盛り線の長さ、幅を変更可能
    '''
    st.subheader("その他")
    '''
    - 右上の︙メニューのSettingsからダークモードに変更可能
    - 表示がおかしくなったりした場合は右上の︙メニューの「Rerun」をクリックすると直るかもしれません

    このソフトは表示フォントに「Noto Sans JP」(https://fonts.google.com/noto/specimen/Noto+Sans+JP) を使用しています。  
    Licensed under SIL Open Font License 1.1 (http://scripts.sil.org/OFL)
    '''

with tab4:
    st.subheader("既知の不具合")
    '''
    
    '''