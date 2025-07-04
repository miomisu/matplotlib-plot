import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm
from sympy import *
from dataclasses import dataclass, field
import toml
import tomllib
import datetime
import pandas as pd
import csv

st.set_page_config(
    page_title="matplotlib GUI",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+JP:wght@400;500;600&display=swap" rel="stylesheet">
<style>
[class^="st-emotion-cache-"] h1,
[class^="st-emotion-cache-"] h2,
[class^="st-emotion-cache-"] h3,
[class^="st-emotion-cache-"] h4,
[class^="st-emotion-cache-"] h5,
[class^="st-emotion-cache-"] h6 {
    font-family: 'IBM Plex Sans JP', sans-serif !important;
    font-weight: 500 !important;
    font-style: normal;
}
[class^="st-emotion-cache-"] h1 {
    font-family: 'IBM Plex Sans JP', sans-serif !important;
    font-weight: 600 !important;
    font-style: normal;
}
body, li, p {
	font-family: 'IBM Plex Sans JP', sans-serif !important;
    font-weight: 400 !important;
    font-style: normal;
}

</style>
""", unsafe_allow_html=True)

st.title("matplotlibで散布図を作成")

tab1, tab2, tab3, tab4 = st.tabs(["基本のプロット", "高度な設定", "使い方", "既知の不具合"])

# ファイル読み込み用関数
@st.cache_data
def get_df(file) -> pd.DataFrame:
    sample = file.read(65536).decode('utf-8')
    file.seek(0)
    dialect = csv.Sniffer().sniff(sample, delimiters=",\t")
    return pd.read_csv(file, delimiter=dialect.delimiter, header=None)

# MARK: クラス作成
@dataclass
class plot_main:
    dpi: int = 300
    width: int = 8
    height: int = 6
    toptick: bool = False
    bottomtick: bool = True
    lefttick: bool = True
    righttick: bool = False
    xtickdir: str = "内側"
    ytickdir: str = "内側"
    property: list = field(default_factory=lambda: [[ 0, 1, "o", 4, 3, "black", "", "marker", 1.0, 1.0,]])
    legends: bool = False
    minorticks: bool = True
    grid: bool = True
    xlog: bool = False
    ylog: bool = False
    xmin: float = None
    xmax: float = None
    ymin: float = None
    ymax: float = None
    xscale: bool = False
    yscale: bool = False
    fontsize: list = field(default_factory=lambda: [12, 12, 12])
    fontfamily: str = ""
    xlabel: str = "X"
    ylabel: str = "Y"
    fp: type = FontProperties
    column: pd.DataFrame = field(default_factory=pd.DataFrame)
    xtick_list_num: list = field(default_factory=list)
    xtick_list: list = field(default_factory=list)
    ytick_list_num: list = field(default_factory=list)
    ytick_list: list = field(default_factory=list)
    ticksetting: bool = True
    xmajor_size: float = 4.0
    ymajor_size: float = 4.0
    xminor_size: float = 2.0
    yminor_size: float = 2.0
    xmajor_width: float = 1.0
    ymajor_width: float = 1.0
    xminor_width: float = 0.6
    yminor_width: float = 0.6
    title: str = "plot"
    expantion: str = ".png" 
    xtick_distance: int = 5
    ytick_distance: int = 5
    
    # MARK: figure作成
    def makefig(self):
        fig = plt.figure(dpi=self.dpi, figsize=(self.width, self.height))
        return fig
    
    # MARK: 目盛り全般設定
    def xtick_settings(self):
        if self.xscale:
            plt.xticks(self.xtick_list_num, self.xtick_list)
        else:
            plt.xticks()
        if self.xtickdir == "内側":
            plt.tick_params(axis='x', which='minor', direction='in', length=self.xminor_size, width=self.xminor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick)
            plt.tick_params(axis="x", which="major", direction='in', length=self.xmajor_size, width=self.xmajor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick, pad=self.xtick_distance, labelfontfamily=self.fontfamily, labelsize=self.fontsize[1])
        elif self.xtickdir == "外側":
            plt.tick_params(axis='x', which='minor', direction='out', length=self.xminor_size, width=self.xminor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick)
            plt.tick_params(axis="x", which="major", direction='out', length=self.xmajor_size, width=self.xmajor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick, pad=self.xtick_distance, labelfontfamily=self.fontfamily, labelsize=self.fontsize[1])
        else:
            plt.tick_params(axis='x', which='minor', direction='inout', length=self.xminor_size, width=self.xminor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick)
            plt.tick_params(axis="x", which="major", direction='inout', length=self.xmajor_size, width=self.xmajor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick, pad=self.xtick_distance, labelfontfamily=self.fontfamily, labelsize=self.fontsize[1])

    def ytick_settings(self):
        if self.yscale:
            plt.yticks(self.ytick_list_num, self.ytick_list)
        else:
            plt.yticks()
        if self.ytickdir == "内側":
            plt.tick_params(axis='y', which='minor', direction='in', length=self.yminor_size, width=self.yminor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick)
            plt.tick_params(axis="y", which="major", direction='in', length=self.ymajor_size, width=self.ymajor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick, pad=self.ytick_distance, labelfontfamily=self.fontfamily, labelsize=self.fontsize[1])
        elif self.ytickdir == "外側":
            plt.tick_params(axis='y', which='minor', direction='out', length=self.yminor_size, width=self.yminor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick)
            plt.tick_params(axis="y", which="major", direction='out', length=self.ymajor_size, width=self.ymajor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick, pad=self.ytick_distance, labelfontfamily=self.fontfamily, labelsize=self.fontsize[1])
        else:
            plt.tick_params(axis='y', which='minor', direction='inout', length=self.yminor_size, width=self.yminor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick)
            plt.tick_params(axis="y", which="major", direction='inout', length=self.ymajor_size, width=self.ymajor_width, bottom=self.bottomtick, top=self.toptick, left=self.lefttick, right=self.righttick, pad=self.ytick_distance, labelfontfamily=self.fontfamily, labelsize=self.fontsize[1])

    # MARK: プロット用関数
    def valueplot2(self):
        for o in self.property:
            temp_column = self.column[[o[0], o[1]]].dropna(subset=[o[0], o[1]]).sort_values(by=o[0])
            temp_column.loc[:, o[0]] *= o[8]
            temp_column.loc[:, o[1]] *= o[9]
            plt.plot(temp_column[o[0]], temp_column[o[1]], o[2], markersize=o[3], linewidth=o[4], c=o[5], label=o[6])

    # MARK: 凡例表示
    def display_legend(self):
        if self.legends:
            plt.legend(fontsize = self.fontsize[2], prop={"family":self.fontfamily, "size":self.fontsize[2]})
    
    # MARK: 補助目盛り追加
    def add_minorticks(self):
        if self.minorticks:
            plt.minorticks_on()
    
    # MARK: グリッド表示
    def display_grid(self):
        if self.grid:
            plt.grid()

    # MARK: x軸対数指定
    def enable_xlog(self):
        if self.xlog:
            plt.xscale("log")
    # MARK: y軸対数指定
    def enable_ylog(self):
        if self.ylog:
            plt.yscale("log")
    
    # MARK: x軸範囲
    def xrange(self):
        if self.xmin != None and self.xmax != None:
            plt.xlim(self.xmin, self.xmax)
    # MARK: y軸範囲
    def yrange(self):
        if self.ymin != None and self.ymax != None:
            plt.ylim(self.ymin, self.ymax)
    
    # MARK: X軸ラベル
    def add_xlabel(self):
        plt.xlabel(self.xlabel, fontfamily = self.fontfamily, fontsize = self.fontsize[0])
    # MARK: Y軸ラベル
    def add_ylabel(self):
        plt.ylabel(self.ylabel, fontfamily = self.fontfamily, fontsize = self.fontsize[0])

    # MARK: NaNの除去
    def removeNaN(self, list):
        return [i for i in list if not np.isnan(i)]
    
    # MARK: NaNを除去したリストの要素数の比較
    def comparison_element(self, list1, list2):
        if len(self.removeNaN(list1)) == len(self.removeNaN(list2)):
            return True
        else:
            return False

# MARK: 辞書のvalueから辞書内での順番を取得
def value_to_index(value: str, dict: dict) -> int:
    try:
        return list(dict.keys()).index([k for k, v in dict.items() if v == value][0])
    except:
        return 0
def select_plottype(value: str, dict1: dict, dict2: dict, plottype: str) -> list:
    if plottype == "marker+line":
        return [value_to_index(value[0], dict1), value_to_index(value[1:], dict2)]
    else:
        return [value_to_index(value, dict1), value_to_index(value, dict2)]
# MARK: マーカーのオプション
colors = ["white", "black", "gray", "lightgrey", "red", "coral", "orangered", "sandybrown", "darkorange", "orange", "gold", "yellow", "lawngreen", "green", "darkgreen", "lime", "aqua", "dodgerblue", "royalblue", "darkblue", "violet", "purple", "magenta", "hotpink"]
markers_dict = {"●": "o", "■": "s", "▼": "v", "▲": "^","◆": "D", "✚": "+", "✖": "x"}
linetype_dict = {"実線":"-", "破線":"--", "点線":":", "一点鎖線":"-."}

# MARK: オブジェクト作成
a = plot_main()
with st.sidebar:
    st.header("基本設定")
    st.subheader("ファイルを選択")
    uploaded_file = st.file_uploader("CSV、VCSV、TSV、TXTファイルを選択", type=["csv", "vcsv", "tsv", "txt"], help="プロットしたい数値データが入っているファイルをアップロードしてください。ファイルの種類は自動判別されます。ファイルサイズの上限は200MBです。")
    if uploaded_file:
        try:
            df = get_df(uploaded_file)
        except Exception as e:
            st.error(f"読み込みに失敗しました: {e}", icon="🚨")
        with st.expander("データを編集"):
            # data_set = st.data_editor(data_set, num_rows="dynamic")
            initial_col_count = len(df.columns)
            new_columns_num = st.number_input("追加する列数", min_value=0, max_value=100, value=0, key=-810)
            for i in range(new_columns_num):
                df[str(initial_col_count+i)] = None
            df = st.data_editor(df)
            a.column = df.apply(pd.to_numeric, errors="coerce")
    # MARK: 設定ファイル読み込み
    st.subheader("設定ファイル読み込み(オプション)")
    setting_file = st.file_uploader("設定ファイルを選択", type=["toml"], help="このアプリで作成したグラフの設定ファイルがある場合はアップロードしてください。")
    if setting_file:
        try:
            settings = tomllib.load(setting_file)
            a.__dict__.update(settings)
        except:
            st.error("正しいファイルを選択できているか確認してください", icon="🚨")
    # MARK: グラフの設定
    st.subheader("グラフの設定")
    col1, col2 = st.columns(2)
    with col1:
        a.xmin = st.number_input("X軸の最小値", value=a.xmin, step=0.1)
    with col2:
        a.xmax = st.number_input("X軸の最大値", value=a.xmax, step=0.1)
    st.caption("両方とも入力すると適用されます")
    st.caption("0.01未満の値を入力した場合0.00と表示されます")
    if a.xmin != None:
        if a.xmax != None:
            if a.xmin > a.xmax:
                st.error("最小値が最大値より大きくなっています", icon="🚨")
    col1, col2 = st.columns(2)
    with col1:
        a.ymin = st.number_input("Y軸の最小値", value=a.ymin, step=0.01)
    with col2:
        a.ymax = st.number_input("Y軸の最大値", value=a.ymax, step=0.01)
    st.caption("両方とも入力すると適用されます")
    st.caption("0.01未満の値を入力した場合0.00と表示されます")
    if a.ymin != None:
        if a.ymax != None:
            if a.ymin > a.ymax:
                st.error("最小値が最大値より大きくなっています", icon="🚨")
    with st.expander("目盛りの詳細設定"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            a.toptick = st.checkbox("上側目盛り", value=a.toptick)
        with col2:
            a.bottomtick = st.checkbox("下側目盛り", value=a.bottomtick)
        with col3:
            a.lefttick = st.checkbox("左側目盛り", value=a.lefttick)
        with col4:
            a.righttick = st.checkbox("右側目盛り", value=a.righttick)
        col1, col2 = st.columns(2)
        with col1:
            a.xtickdir = st.radio("X軸の目盛りの向き", ["内側", "外側", "両方"], horizontal=True, index=["内側", "外側", "両方"].index(a.xtickdir))
        with col2:
            a.ytickdir = st.radio("Y軸の目盛りの向き", ["内側", "外側", "両方"], horizontal=True, index=["内側", "外側", "両方"].index(a.ytickdir))
        a.xscale = st.checkbox("X軸の目盛りの位置を設定", value=a.xscale)
        xtick = st.text_input("目盛りを表示する位置(数値)をスペースで区切って入力", key = "xtick", value=' '.join(a.xtick_list))
        a.xtick_list = xtick.split()
        try:
            a.xtick_list_num = [float(i) for i in a.xtick_list]
        except:
            st.error("数値を入力してください", icon="🚨")
        a.yscale = st.checkbox("Y軸の目盛りの位置を設定", value=a.yscale)
        ytick = st.text_input("目盛りを表示する位置(数値)をスペースで区切って入力", key = "ytick", value=' '.join(a.ytick_list))
        a.ytick_list = ytick.split()
        try:
            a.ytick_list_num = [float(i) for i in a.ytick_list]
        except:
            st.error("数値を入力してください", icon="🚨")
        col1, col2 = st.columns(2)
        with col1:
            a.xtick_distance= st.number_input("X軸目盛りラベルと軸の距離", min_value=0, value=a.xtick_distance, step=1)
        with col2:
            a.ytick_distance= st.number_input("Y軸目盛りラベルと軸の距離", min_value=0, value=a.ytick_distance, step=1)
        a.minorticks = st.checkbox("補助目盛り", value=a.minorticks)
    col1, col2 = st.columns(2)
    with col1:
        a.xlabel = st.text_input("X軸のラベル", value=a.xlabel)
    with col2:
        a.ylabel = st.text_input("Y軸のラベル", value=a.ylabel)
    st.caption("\$で囲むことで$\LaTeX$記法の数式を使用可能です")
    col1, col2 = st.columns(2)
    with col1:
        a.xlog = st.checkbox("X軸を対数軸にする", value=a.xlog)
        a.legends = st.checkbox("凡例表示", value=a.legends)
    with col2:
        a.ylog = st.checkbox("Y軸を対数軸にする", value=a.ylog)
        a.grid = st.checkbox("グリッド", value=a.grid)
    # MARK: フォント指定
    col1, col2, col3 = st.columns(3)
    fm.fontManager.addfont(r"HaranoAjiGothic-Regular.otf")
    fm.fontManager.addfont(r"HaranoAjiMincho-Regular.otf")
    with col1:
        a.fontsize[0] = st.number_input("ラベルのフォントサイズ", min_value=0, step=1, value=a.fontsize[0])
    with col2:
        a.fontsize[1] = st.number_input("目盛りのフォントサイズ", min_value=0, step=1, value=a.fontsize[1])
    with col3:
        a.fontsize[2] = st.number_input("凡例のフォントサイズ", min_value=0, step=1, value=a.fontsize[2])
    fontstyle = st.radio("フォントスタイル", ["明朝体", "ゴシック体"], horizontal=True)
    if fontstyle == "明朝体":
        a.fontfamily = "Harano Aji Mincho"
        plt.rcParams["mathtext.fontset"] = "cm"
    if fontstyle == "ゴシック体":
        a.fontfamily = "Harano Aji Gothic"
        plt.rcParams["mathtext.fontset"] = "stixsans"
    yaxis = []
    if uploaded_file:
        st.header("プロットするデータ系列")
        number_of_data = st.number_input("プロットするデータ系列の数", min_value=0, step=1, value=len(a.property))
        a.property += [[ 0, 1, "o", 4, 3, "black", "", "marker", 1.0, 1.0,] for i in range(number_of_data - 1)]
        property_ = [[] for i in range(number_of_data)]
        # プロットするデータ系列の数だけ設定を用意
        for y in range(number_of_data):
            st.write("**データ系列" + str(y + 1) + "**")
            col1, col2 = st.columns(2)
            with col1:
                xa = st.selectbox("Xとする列", a.column.columns.tolist(), index=int(a.property[y][0]), key=y + 0.01)
                property_[y].append(xa)
            with col2:
                ya = st.selectbox("Yとする列", a.column.columns.tolist(), index=int(a.property[y][1]), key=y + 0.02)
                property_[y].append(ya)
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.markdown("Xの値を")
            with col2:
                x_magnification = st.number_input("a", label_visibility="collapsed", value=a.property[y][8], key=y + 0.011)
            with col3:
                st.markdown("倍する")
            with col4:
                st.markdown("Yの値を")
            with col5:
                y_magnification = st.number_input("a", label_visibility="collapsed", value=a.property[y][9], key=y + 0.012)
            with col6:
                st.markdown("倍する")
            if xa == ya:
                st.error("X軸とY軸で同じ列を選択しています", icon="🚨")
            if a.property[y][7] == "marker+line":
                plottype_index = 2
            elif a.property[y][7] == "line":
                plottype_index = 1
            else:
                plottype_index = 0
            plottype = st.radio("プロットの種類", ["マーカー", "折れ線", "両方"], horizontal=True, key=y + 0.05, index=plottype_index)
            col1, col2, col3= st.columns(3)
            with col1:
                marker = st.selectbox("マーカーの形", (markers_dict.keys()), key=y + 0.03, index=select_plottype(a.property[y][2], markers_dict, linetype_dict, a.property[y][7])[0])
                linetype = st.selectbox("線の種類", (linetype_dict.keys()), key=y + 0.04, index=select_plottype(a.property[y][2], markers_dict, linetype_dict, a.property[y][7])[1])
                if plottype == "マーカー":
                    property_[y].append(markers_dict[marker])
                elif plottype == "折れ線":
                    property_[y].append(linetype_dict[linetype])
                elif plottype == "両方":
                    property_[y].append(markers_dict[marker] + linetype_dict[linetype])
            with col2:
                markersize = st.number_input("マーカーの大きさ", value=a.property[y][3], min_value=0, step=1, key=y + 0.06)
                property_[y].append(markersize)
                linewidth = st.number_input("線の幅", value=a.property[y][4], min_value=0, step=1, key=y + 0.07)
                property_[y].append(linewidth)
            with col3:
                color = st.selectbox("色", (colors), key=y + 0.08, index=colors.index(a.property[y][5]))
                property_[y].append(color)
                legend = st.text_input("凡例名", key=y + 0.09, value=a.property[y][6])
                property_[y].append(legend)
            if plottype == "マーカー":
                    property_[y].append("marker")
            elif plottype == "折れ線":
                property_[y].append("line")
            elif plottype == "両方":
                property_[y].append("marker+line")
            property_[y].append(x_magnification)
            property_[y].append(y_magnification)
            property_[y].append(y + 1)
            '''
            ---
            '''
        a.property = property_
        st.write("グラフのサイズ")
        col1, col2, col3= st.columns(3)
        with col1:
            a.dpi = st.number_input("dpi", value=a.dpi, step=1, min_value=10)
        with col2:
            a.width = st.number_input("幅(インチ)", value=a.width, step=1, min_value=1)
        with col3:
            a.height = st.number_input("高さ(インチ)", value=a.height, step=1, min_value=1)
        st.write("サイズ(余白削除前)  :    " + str(a.width * a.dpi) + "×" + str(a.height * a.dpi))
        col1, col2 = st.columns(2)
        with col1:
            a.title = st.text_input("保存するファイル名", a.title)
        with col2:
            a.expantion = st.selectbox("保存する拡張子", (".png", ".jpg", ".svg", ".pdf"), index=[".png", ".jpg", ".svg", ".pdf"].index(a.expantion))
        st.caption("svg, pdfの場合プロットする点が多いと保存した画像が重くなるので注意")

with tab1:
    st.write("←サイドバーを開いて設定を表示(サイズ変更可能)")
    #st.write(plt.style.available)
    #st.write(matplotlib.matplotlib_fname())
    if uploaded_file:
        # プロット
        fig = a.makefig()
        plt.rcParams["grid.linewidth"] = 0.8
        plt.rcParams["axes.linewidth"] = 0.8
        plt.rcParams["grid.color"] = "#b0b0b0"
        plt.rcParams['axes.axisbelow'] = True
        a.xtick_settings()
        a.ytick_settings()
        a.valueplot2()
        a.display_legend()
        a.add_minorticks()
        a.display_grid()
        a.enable_xlog()
        a.enable_ylog()
        a.xrange()
        a.yrange()
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
    else:
        st.markdown("データをアップロードするとグラフが表示されます")
    # MARK: 設定保存
    filtered_settings = {
        key: value
        for key, value in vars(a).items()
        # nullとtype型の変数を除去
        if not isinstance(value, type) and value is not None
        # プロットデータを除去
        if key not in ["column"]
    }
    date_str_hyphen = datetime.date.today().strftime("%Y-%m-%d")
    with open(f"graph_settings_{date_str_hyphen}.toml", "w+", encoding="utf-8") as f:
        f.write(toml.dumps(filtered_settings))
        f.seek(0)
        btn=st.download_button(
            label="グラフの設定を保存",
            data=f,
            file_name=f"graph_settings_{date_str_hyphen}.toml",
            help="現在のグラフの設定を再現できるようにグラフのプロパティが記録された設定ファイルをダウンロードします。"
        )
    '''
    **更新履歴**
    - ファイルの種類を自動判別するように変更(2025/06/21)
    - X、Yの値を定数倍する機能を追加(2025/06/16)
    - グラフの設定のエクスポート・インポート機能を追加(2025/06/04)
    - アップロードしたデータを編集できるように変更(2025/04/25)
    - 数式のフォントを変更(2024/12/26)
    - 関数の入力方法を変更(2024/11/30)
    - 凡例に日本語を表示できるように変更(2024/11/26)
    - グラフ全体のフォントを明朝体とゴシック体で切り替えられるように変更(2024/11/26)
    - フォントサイズをラベル、目盛り、凡例で個別に指定できるように変更(2024/05/24)
    - Xの値として複数の列を指定できるように変更(2024/05/23)
    - 近似式の係数の順番が逆になっていたのを修正(2024/05/23)
    - 近似直線・近似曲線の表示機能を追加(2024/05/22)
    - プロットがグリッドより手前に描画されるように変更(2024/05/22)
    '''


with tab2:
    st.subheader("高度な設定")
    with st.container(height=450):
        with st.expander("ユーザー関数を表示"):
            setfunction = st.checkbox(":orange-background[有効化]", value=False, key="function")
            f = st.text_input("表示したいxの関数を入力", placeholder="例) sin(x)+cos(x), x**2 - 4*x + 3, log(x)")
            st.caption("SymPyの関数・定数を利用可能です。https://pianofisica.hatenablog.com/entry/2021/04/23/190000 などを参考にして、`sympy.`または`sp.`を除いて入力してください。累乗はアスタリスク2つ`**`で表します。")
            st.write("表示する範囲(入力必須)")
            # オプション
            f_min = 0
            f_max = 1
            slice = 1
            if uploaded_file:
                col1, col2, col3 = st.columns(3)
                with col1:
                    f_min = st.number_input("最小値", value=np.min(a.removeNaN(a.column[a.property[0][0]])), step=0.01)
                with col2:
                    f_max = st.number_input("最大値", value=np.max(a.removeNaN(a.column[a.property[0][0]])), step=0.01)
                with col3:
                    slice = st.number_input("分割数(滑らかさ)", value=100, min_value=0, step=1)

            st.write("オプション")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                f_linetype = st.selectbox("線の種類", (linetype_dict.keys()))
            with col2:
                f_color = st.selectbox("色", (colors), index=1)
            with col3:
                f_size = st.number_input("線の幅", value=3.0, min_value=0.0, step=0.5)
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
                    func = sympify(f)
                    y = [func.subs('x', val) for val in x]
                except:
                    st.error("関数を正しく入力できているか確認してください", icon="🚨")

        with st.expander("近似直線・近似曲線を表示"):
            setapprox = st.checkbox(":orange-background[有効化]", value=False, key="setapprox")
            if uploaded_file:
                yaxis = [r + 1 for r in range(len(a.property))]
            approxdata =  st.multiselect("近似するデータ系列を選択", yaxis, default=None)
            approxproperty = [[] for i in range(len(approxdata))]
            for i, o in enumerate(approxdata):
                # MARK: NaNの項目を除去
                temp_column = a.column[[a.property[o-1][0], a.property[o-1][1]]].dropna(subset=[a.property[o-1][0], a.property[o-1][1]]).sort_values(by=a.property[o-1][0])
                temp_column.loc[:, str(a.property[o-1][0])] *= a.property[o-1][8]
                temp_column.loc[:, str(a.property[o-1][1])] *= a.property[o-1][9]
                st.write("データ系列" + str(o))
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    approx_dim = st.number_input("次数を入力", min_value=1, step=1, value=1, key=-1 * o -0.4)
                    approxproperty[i].append(approx_dim)
                coefficient = np.polyfit(temp_column[str(a.property[o-1][0])], temp_column[str(a.property[o-1][1])], approx_dim)
                approxproperty[i].append(coefficient)
                # 数式表示
                coefficient_str = []
                for q, j in enumerate(coefficient):
                    if j > 0 and q == len(coefficient) - 1:
                        coefficient_str.append("+" + str(round(j, 3)))
                    elif j <= 0 and q == len(coefficient) - 1:
                        coefficient_str.append("-" + str(round(j, 3)))
                    elif j > 0 and q == len(coefficient) - 2:
                        coefficient_str.append("+" + str(round(j, 3)) + "x")
                    elif j <= 0 and q == len(coefficient) - 2:
                        coefficient_str.append("-" + str(round(-1 * j, 3)) + "x")
                    elif j >= 0 and q == 0:
                        coefficient_str.append(str(round(j, 3)) + "x^" + str(len(coefficient) - 1))
                    elif j >= 0:
                        coefficient_str.append("+" + str(round(j, 3)) + "x^" + str(len(coefficient) - q - 1))
                    elif j < 0:
                        coefficient_str.append("-" + str(round(-1 * j, 3)) + "x^" + str(len(coefficient)- q - 1))
                formula = "$"
                for p in range(len(coefficient)):
                    formula += coefficient_str[p]
                formula += "$"
                st.write("近似式: " + formula)

                st.write("表示する範囲")
                col1, col2, col3 = st.columns(3)
                with col1:
                    min = st.number_input("最小値", value=temp_column[str(a.property[o-1][0])].min(), step=0.01, key=i + 10.1)
                with col2:
                    max = st.number_input("最大値", value=temp_column[str(a.property[o-1][0])].max(), step=0.01, key=i + 10.01)
                with col3:
                    slice = st.number_input("分割数(滑らかさ)", value=100, min_value=0, step=1, key=i + 10.001)
                approx_x = np.linspace(min, max, slice)
                approxproperty[i].append(approx_x)
                approxproperty[i].append(np.polyval(coefficient, approx_x))

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    approx_linetype = st.selectbox("線の種類", (linetype_dict.keys()), key=-1 * o)
                    approxproperty[i].append(approx_linetype)
                with col2:
                    approx_color = st.selectbox("色", (colors), index=1, key=-1 * o - 0.1)
                    approxproperty[i].append(approx_color)
                with col3:
                    approx_width = st.number_input("線の幅", value=3.0, min_value=0.0, step=0.5, key=-1 * o - 0.2)
                    approxproperty[i].append(approx_width)
                with col4:
                    approx_legend = st.text_input("凡例名", key=-1 * o - 0.3)
                    approxproperty[i].append(approx_legend)


        with st.expander("フォントを指定する(軸ラベルのみ)"):
            setfont = st.checkbox(":orange-background[有効化]", value=False, disabled=True, key="font")
            fontpath = st.text_input("フォントファイルのパスを指定", placeholder="例) C:\Windows\Fonts\HGRPP1.ttc")
            if fontpath:
                fp = FontProperties(fname=fontpath, size=a.fontsize[0])
            st.caption("システムフォントの場所 C:\\Windows\\Fonts ユーザーフォントの場所 C:\\Users\\ユーザー名\\AppData\\Local\\Microsoft\\Windows\\Fonts")
        
        with st.expander("目盛り線の設定"):
            a.ticksetting = st.checkbox(":orange-background[有効化]", value=False, key="ticksetting")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                a.xmajor_size = st.number_input("X軸主目盛り線長さ", value=4.0, step=0.1, min_value=0.0)
                a.ymajor_size = st.number_input("Y軸主目盛り線長さ", value=4.0, step=0.1, min_value=0.0)
            with col2:
                a.xminor_size = st.number_input("X軸補助目盛り線長さ", value=2.0, step=0.1, min_value=0.0)
                a.yminor_size = st.number_input("Y軸補助目盛り線長さ", value=2.0, step=0.1, min_value=0.0)
            with col3:
                a.xmajor_width = st.number_input("X軸主目盛り線幅", value=1.0, step=0.1, min_value=0.0)
                a.ymajor_width = st.number_input("Y軸主目盛り線幅", value=1.0, step=0.1, min_value=0.0)
            with col4:
                a.xminor_width = st.number_input("X軸補助目盛り線幅", value=0.6, step=0.1, min_value=0.0)
                a.yminor_width = st.number_input("Y軸補助目盛り線幅", value=0.6, step=0.1, min_value=0.0)

        with st.expander("凡例の詳細設定"):
            legendloc_dict = {"自動": "best", "内側左上": "upper left", "内側中央上": "upper center", "内側右上": "upper right", "内側中央左": "center left", "内側中央": "center", "内側中央右": "center right", "内側左下": "lower left", "内側中央下": "lower center", "内側右下": "lower right", "外側中央上": ["lower center", 0.5, 1], "外側右上": ["upper left", 1, 1.02], "外側右中央": ["center left", 1, 0.5], "外側右下": ["lower left", 1, -0.015],"外側中央下": ["upper center", 0.5, -0.1] }
            legendsetting = st.checkbox(":orange-background[有効化]", value=False, key="legendsetting")
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
            legendloc = st.selectbox("位置", (legendloc_dict))

        with st.expander("グリッドの設定"):
            gridsettings = st.checkbox(":orange-background[有効化]", value=False, key="gridsettings")
            xgrid = st.radio("X軸のグリッド位置", ["なし", "主目盛り", "補助目盛り", "両方"], index=1, horizontal=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                xmajorgridtype = st.selectbox("X軸主目盛りグリッド種類", (linetype_dict.keys()))
                xminorgridtype = st.selectbox("X軸補助目盛りグリッド種類", (linetype_dict.keys()))
            with col2:
                xmajorgridwidth = st.number_input("X軸主目盛りグリッド線幅", value=0.8, min_value=0.0, step=0.1)
                xminorgridwidth = st.number_input("X軸補助目盛りグリッド線幅", value=0.8, min_value=0.0, step=0.1)
            with col3:
                xmajorgridcolor = st.selectbox("X軸主目盛りグリッドの色", (colors), index=None)
                if xmajorgridcolor == None:
                    xmajorgridcolor = "#b0b0b0"
                xminorgridcolor = st.selectbox("X軸補助目盛りグリッドの色", (colors), index=None)
                if xminorgridcolor == None:
                    xminorgridcolor = "#b0b0b0"

            ygrid = st.radio("Y軸のグリッド位置", ["なし", "主目盛り", "補助目盛り", "両方"], index=1, horizontal=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                ymajorgridtype = st.selectbox("Y軸主グリッド種類", (linetype_dict.keys()))
                yminorgridtype = st.selectbox("Y軸補助目盛りグリッド種類", (linetype_dict.keys()))
            with col2:
                ymajorgridwidth = st.number_input("Y軸主目盛りグリッド線幅", value=0.8, min_value=0.0, step=0.1)
                yminorgridwidth = st.number_input("Y軸補助目盛りグリッド線幅", value=0.8, min_value=0.0, step=0.1)
            with col3:
                ymajorgridcolor = st.selectbox("Y軸主目盛りグリッドの色", (colors), index=None)
                if ymajorgridcolor == None:
                    ymajorgridcolor = "#b0b0b0"
                yminorgridcolor = st.selectbox("Y軸補助目盛りグリッドの色", (colors), index=None)
                if yminorgridcolor == None:
                    yminorgridcolor = "#b0b0b0"

        with st.expander("その他の設定"):
            setframewidh = st.checkbox("グラフの枠の幅を設定", value=False)
            framewidth = st.number_input("グラフの枠の幅", value=0.8, min_value=0.0, step=0.1, disabled=not setframewidh)

    if setfunction or setfont or a.ticksetting or gridsettings or legendsetting or setframewidh or setapprox:
        if uploaded_file:
            adv_fig = a.makefig()
            plt.rcParams['axes.axisbelow'] = True
            # 設定適用
            if setfunction and f and f_max > f_min:
                plt.plot(x, y, linetype_dict[f_linetype], c=f_color, linewidth=f_size, label=f_legend)
            if setframewidh:
                plt.rcParams["axes.linewidth"] = framewidth

            # 近似直線
            if setapprox:
                for g in approxproperty:
                    if g[0]:
                        plt.plot(g[2], g[3], linetype_dict[g[4]], c=g[5], linewidth=g[6], label=g[7])

            a.xtick_settings()
            a.ytick_settings()
            a.valueplot2()
            if legendsetting:
                if "外側" in legendloc:
                    plt.legend(fontsize=a.fontsize[2], prop={"family":a.fontfamily, "size":a.fontsize[2]}, frameon=legend_frame, fancybox=legend_corner, facecolor=legend_color, framealpha=legend_transparency, edgecolor=legend_framecolor, ncol=legend_cols, labelcolor=legend_lettercolor, loc=legendloc_dict[legendloc][0], bbox_to_anchor=(legendloc_dict[legendloc][1], legendloc_dict[legendloc][2]))
                else:
                    plt.legend(fontsize=a.fontsize[2], prop={"family":a.fontfamily, "size":a.fontsize[2]}, frameon=legend_frame, fancybox=legend_corner, facecolor=legend_color, framealpha=legend_transparency, edgecolor=legend_framecolor, ncol=legend_cols, labelcolor=legend_lettercolor, loc=legendloc_dict[legendloc])
            else:
                a.display_legend()
            a.add_minorticks()
            if gridsettings:
                if xgrid == "主目盛り":
                    plt.grid(which="major", axis="x", linestyle=linetype_dict[xmajorgridtype], c=xmajorgridcolor, linewidth=xmajorgridwidth)
                elif xgrid == "補助目盛り":
                    plt.grid(which="minor", axis="x", linestyle=linetype_dict[xminorgridtype], c=xminorgridcolor, linewidth=xminorgridwidth)
                elif xgrid == "両方":
                    plt.grid(which="major", axis="x", linestyle=linetype_dict[xmajorgridtype], c=xmajorgridcolor, linewidth=xmajorgridwidth)
                    plt.grid(which="minor", axis="x", linestyle=linetype_dict[xminorgridtype], c=xminorgridcolor, linewidth=xminorgridwidth)
                if ygrid == "主目盛り":
                    plt.grid(which="major", axis="y", linestyle=linetype_dict[ymajorgridtype], c=ymajorgridcolor, linewidth=ymajorgridwidth)
                elif ygrid == "補助目盛り":
                    plt.grid(which="minor", axis="y", linestyle=linetype_dict[yminorgridtype], c=yminorgridcolor, linewidth=yminorgridwidth)
                elif ygrid == "両方":
                    plt.grid(which="major", axis="y", linestyle=linetype_dict[ymajorgridtype], c=ymajorgridcolor, linewidth=ymajorgridwidth)
                    plt.grid(which="minor", axis="y", linestyle=linetype_dict[yminorgridtype], c=yminorgridcolor, linewidth=yminorgridwidth)
            else:
                a.display_grid()
            a.enable_xlog()
            a.enable_ylog()
            a.xrange()
            a.yrange()
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
    4. プロットするデータを選択する
        - データ系列を追加してX、Yとするデータの列を選択する
        - データ系列を追加するとそのデータ系列の表示設定が表示されるので変更する
        - XとYの列の要素数が等しくない場合折れ線グラフは表示不可
    5. 保存する画像の設定を変更する
        - dpi=1インチあたりのドット数
        - ベクター形式のpdf、svgで保存すると拡大しても粗くならないが、プロットする点が極端に多い場合保存した画像の読み込みなどが重くなることがあるので注意
    6. 画像を保存する
        - 設定を変更して完成したら「画像を保存」ボタンを押して画像をダウンロードできる
    7. 設定の保存と読み込み
        - グラフを作成して設定を変更した後に「グラフの設定を保存」ボタンを押すとサイドバーでの設定内容がtomlファイルに出力される
        - 新しくグラフを作成する際にプロット用のデータを読み込んで設定ファイルを読み込むと設定を再現できる
    '''
    st.subheader("高度な設定")
    '''
    - 関数を表示
        - 散布図に関数のグラフを表示可能
        - xを変数とした関数を入力する
        - 一般的な数式のように四則演算を入力可能 足し算:`+` 引き算:`-`  掛け算`*` 割り算:`/` 累乗:`**`
        - 三角関数や対数関数などはnumpyというライブラリの表記に従って入力する
    - 近似直線・近似曲線を表示
        - 近似直線・近似曲線と近似式を表示可能
        - 近似するデータ系列と近似の次数、プロットのオプションを選択
        - XとYの列の要素数が等しくない場合表示不可
    - フォントの指定
        - 開発中
    - 目盛り線の設定
        - 各軸の主、補助目盛り線の長さ、幅を変更可能
    - 凡例の詳細設定
        - 凡例の枠、背景、色、位置などを変更可能
    - グリッドの設定
        - グリッドの位置、種類、線幅、色を変更可能
    - その他の設定
        - グラフの枠の幅を変更可能
    '''
    st.subheader("その他")
    '''
    - 右上の︙メニューのSettingsからダークモードに変更可能
    - 表示がおかしくなったりした場合は右上の︙メニューの「Rerun」をクリックすると直るかもしれません

    このプログラムは「原ノ味フォント」(https://github.com/trueroad/HaranoAjiFonts) を使用しています。  
    Licensed under SIL Open Font License 1.1 (http://scripts.sil.org/OFL)
    '''

with tab4:
    st.subheader("既知の不具合")
    '''
    
    '''
    # import matplotlib.font_manager as fm
    # font_list = sorted(fm.get_font_names())
    # st.write(font_list)