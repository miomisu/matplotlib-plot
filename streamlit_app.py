import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.font_manager import FontProperties

st.title("matplotlibで散布図を作成")

tab1, tab2, tab3, tab4 = st.tabs(["基本のプロット", "高度な設定", "使い方", "既知のバグ"])

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

# プロット用関数
def plot(dpi, width, height, toptick, bottomtick, lefttick, righttick, xtickdir, ytickdir, property, legends, ja_legends, minorticks, grid, xlog, ylog, xmin, xmax, ymin, ymax, xscale, yscale, fontsize, xlabel, ylabel, fp, column, xaxis, xtick_list_num, xtick_list, ytick_list_num, ytick_list, ticksetting = False, xmajor_size = 4.0, ymajor_size = 4.0, xminor_size = 2.0, yminor_size = 2.0, xmajor_width = 1.0, ymajor_width = 1.0, xminor_width = 0.6, yminor_width = 0.6) -> matplotlib.figure.Figure:
    # プロット
    fig = plt.figure(dpi=dpi, figsize=(width, height))

    # 目盛り有無
    plt.rcParams["xtick.top"] = toptick
    plt.rcParams["xtick.bottom"] = bottomtick
    plt.rcParams["ytick.left"] = lefttick
    plt.rcParams["ytick.right"] = righttick

    # 目盛り向き
    if xtickdir == "内側":
        plt.rcParams["xtick.direction"] = "in"
    elif xtickdir == "外側":
        plt.rcParams["xtick.direction"] = "out"
    else:
        plt.rcParams["xtick.direction"] = "inout"

    if ytickdir == "内側":
        plt.rcParams["ytick.direction"] = "in"
    elif ytickdir == "外側":
        plt.rcParams["ytick.direction"] = "out"
    else:
        plt.rcParams["ytick.direction"] = "inout"

    # 目盛り線
    # st.write(ticksetting)
    # st.write(xmajor_size)
    if ticksetting:
        plt.rcParams["xtick.major.size"] = xmajor_size
        plt.rcParams["ytick.major.size"] = ymajor_size
        plt.rcParams["xtick.minor.size"] = xminor_size
        plt.rcParams["ytick.minor.size"] = yminor_size
        plt.rcParams["xtick.major.width"] = xmajor_width
        plt.rcParams["ytick.major.width"] = ymajor_width
        plt.rcParams["xtick.minor.width"] = xminor_width
        plt.rcParams["ytick.minor.width"] = yminor_width

    # 値プロット
    for o in property:
        if o[5] == False:
            plt.scatter(column[xaxis], column[o[0]], c = o[1], marker = o[2], s = o[3], label = o[4])
        else:
            if any(np.isnan(column[o[0]])):
                st.write("第" + str(o[0]) + "列に欠損値があるため折れ線グラフを表示できません。")
            else:
                plt.plot(column[xaxis], column[o[0]], c = o[1], linewidth = o[3], label = o[4])
    # 凡例表示
    if legends == True and ja_legends == False:
        plt.legend(fontsize = fontsize)
    if legends == True and ja_legends == True:
        plt.legend(fontsize = fontsize, prop={"family":"Meiryo"})
    
    # 副目盛り追加
    if minorticks:
        plt.minorticks_on()
    
    # グリッド表示
    if grid:
        plt.grid()
    # x軸対数指定
    if xlog:
        plt.xscale("log")
    # y軸対数指定
    if ylog:
        plt.yscale("log")
    
    # x軸範囲
    if xmin != None and xmax != None:
        plt.xlim(xmin, xmax)
    # y軸範囲
    if ymin != None and ymax != None:
        plt.ylim(ymin, ymax)
    # 軸目盛り
    if xscale:
        plt.xticks(xtick_list_num, xtick_list, fontsize = fontsize)
    else:
        plt.xticks(fontsize = fontsize)
    if yscale:
        plt.yticks(ytick_list_num, ytick_list, fontsize = fontsize)
    else:
        plt.yticks(fontsize = fontsize)
    # X軸ラベル
    plt.xlabel(xlabel, fontproperties = fp)
    # Y軸ラベル
    plt.ylabel(ylabel, fontproperties=fp)

    return fig

# マーカーのオプション
colors = ["black", "gray", "lightgrey", "red", "coral", "orangered", "sandybrown", "darkorange", "orange", "gold", "yellow", "lawngreen", "green", "darkgreen", "lime", "aqua", "dodgerblue", "royalblue", "darkblue", "violet", "purple", "magenta", "hotpink"]
markers = ["o", ",", "v", "^", "D", "+", "x"]


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
            xmin = st.number_input("X軸の最小値", value=None, step=0.1)
        with col2:
            xmax = st.number_input("X軸の最大値", value=None, step=0.1)
        st.caption("両方とも入力していない場合自動で調整されます")
        if xmin != None:
            if xmax != None:
                if xmin > xmax:
                    st.error("最小値が最大値より大きくなっています", icon="🚨")

        col1, col2 = st.columns(2)
        with col1:
            ymin = st.number_input("Y軸の最小値", value=None, step=0.01)

        with col2:
            ymax = st.number_input("Y軸の最大値", value=None, step=0.01)
        st.caption("両方とも入力していない場合自動で調整されます")
        if ymin != None:
            if ymax != None:
                if ymin > ymax:
                    st.error("最小値が最大値より大きくなっています", icon="🚨")

        with st.expander("目盛りの詳細設定"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                toptick = st.checkbox("上側目盛り", value=False)
            with col2:
                bottomtick = st.checkbox("下側目盛り", value=True)
            with col3:
                lefttick = st.checkbox("左側目盛り", value=True)
            with col4:
                righttick = st.checkbox("右側目盛り", value=False)

            col1, col2 = st.columns(2)
            with col1:
                xtickdir = st.radio("X軸の目盛りの向き", ["内側", "外側", "両方"], horizontal=True, index=0)
            with col2:
                ytickdir = st.radio("Y軸の目盛りの向き", ["内側", "外側", "両方"], horizontal=True, index=0)

            xscale = st.checkbox("X軸の目盛りの位置を設定", value = False)
            xtick_list = []
            xtick_list_num = []
            if xscale:
                xtick = st.text_input("目盛りを表示する位置(数値)をスペースで区切って入力", key = "xtick")
                xtick_list = xtick.split()
                try:
                    xtick_list_num = [float(i) for i in xtick_list]
                except:
                    st.error("数値を入力してください", icon="🚨")

            yscale = st.checkbox("Y軸の目盛りの位置を設定", value = False)
            ytick_list = []
            ytick_list_num = []
            if yscale:
                ytick = st.text_input("目盛りを表示する位置(数値)をスペースで区切って入力", key = "ytick")
                ytick_list = ytick.split()
                try:
                    ytick_list_num = [float(i) for i in ytick_list]
                except:
                    st.error("数値を入力してください", icon="🚨")

            minorticks = st.checkbox("副目盛り", value="True")

        col1, col2 = st.columns(2)
        with col1:
            xlabel = st.text_input("X軸のラベル", "X")
        with col2:
            ylabel = st.text_input("Y軸のラベル", "Y")
        st.caption("$で囲むことでTeX記法の数式を使用可能")

        col1, col2 = st.columns(2)
        with col1:
            xlog = st.checkbox("X軸を対数軸にする", value=False)
            legends = st.checkbox("凡例表示", value=False)
            ja_legends = False
            if legends:
                ja_legends = st.checkbox("凡例名に日本語を用いる", value = False)
            # フォント指定
            fontsize = st.number_input("フォントサイズ", step=1, value=12)
            fp = FontProperties(fname=r"C:\Windows\Fonts\meiryo.ttc", size=fontsize)

        with col2:
            ylog = st.checkbox("Y軸を対数軸にする", value=False)
            grid = st.checkbox("グリッド", value="True")



        if uploaded_file:
            #data_set = get_data(uploaded_file)
            # st.write(uploaded_file.name)
            columns = []
            # 行列入れ替え
            column = [[] for i in range(len(data_set[0]))]
            for i in range(len(data_set[0])):
                columns.append(i)
                for j in range(len(data_set)):
                    column[i].append(data_set[j][i])

            # st.write(data_set[0])
            # st.write(type(data_set))

            col1, col2 = st.columns(2)
            with col1:
                xaxis = st.selectbox("X軸とする列", columns)
            with col2:
                yaxis = st.multiselect("Y軸とする列（複数選択可）", columns)
            if xaxis in yaxis:
                st.error("X軸とY軸で同じ列を選択しています", icon="🚨")

            # プロットオプション
            #if yaxis != None:
            if xaxis not in yaxis:
                if yaxis:
                    st.write("マーカーのオプション")
                property = [[] for i in range(len(yaxis))]
                for i, ycolumn in enumerate(yaxis):
                    property[i].append(ycolumn)
                    st.write("第" + str(ycolumn) + "列")
                    poly = st.checkbox("折れ線グラフにする", value = False, key = i + 0.4)
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        color = st.selectbox("色を選択", (colors), key = i)
                        property[i].append(color)
                    with col2:
                        marker = st.selectbox("形を選択", (markers), key = i + 0.1, disabled = poly)
                        property[i].append(marker)
                    with col3:
                        size = st.number_input("大きさを入力", value = 20, min_value = 0, step = 1, key = i + 0.2)
                        property[i].append(size)
                    with col4:
                        legend = st.text_input("凡例名を入力", key = i + 0.3)
                        property[i].append(legend)
                    property[i].append(poly)
                #st.write(property)
            st.write("グラフのサイズ")
            col1, col2, col3= st.columns(3)
            with col1:
                dpi = st.number_input("dpi", value = 300, step = 1, min_value = 10)
            with col2:
                width = st.number_input("幅(インチ)", value = 8, step = 1, min_value = 1)
            with col3:
                height = st.number_input("高さ(インチ)", value = 6, step = 1, min_value = 1)
            st.write("サイズ(余白削除前)      " + str(width * dpi) + "×" + str(height * dpi))

            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("保存するファイル名", "plot")
            with col2:
                expantion = st.selectbox("保存する拡張子", (".png", ".jpg", ".svg", ".pdf"))
            st.caption("svg, pdfの場合プロットする点が多いと保存した画像が重くなるので注意")

    st.write("←サイドバーを開く(サイズ変更可能)")
    if uploaded_file:
        # プロット
        fig = plot(dpi, width, height, toptick, bottomtick, lefttick, righttick, xtickdir, ytickdir, property, legends, ja_legends, minorticks, grid, xlog, ylog, xmin, xmax, ymin, ymax, xscale, yscale, fontsize, xlabel, ylabel, fp, column, xaxis, xtick_list_num, xtick_list, ytick_list_num, ytick_list)
        # 表示
        st.pyplot(fig)
        # 保存
        plt.savefig(title + expantion, bbox_inches="tight")
        # ダウンロード
        with open(title + expantion, "rb") as file:
            btn = st.download_button(
                label = "画像を保存",
                data = file,
                file_name = title + expantion,
                )


with tab2:
    st.subheader("高度な設定")
    # 関数を表示
    function = st.checkbox("関数を表示", value = False)
    if function:
        f = st.text_input("表示したいxの関数を入力", placeholder = "例) np.sin(x), x**2 - 4*x + 3")
        st.caption("累乗はアスタリスク2つ(**)で表す 三角関数等はhttps://deepage.net/features/numpy-math.html などを参照")
        st.write("表示する範囲(入力必須)")
        # オプション
        col1, col2, col3 = st.columns(3)
        with col1:
            f_min = st.number_input("最小値", value=0.0, step=0.01)
            f_color = st.selectbox("色を選択", (colors))
        with col2:
            f_max = st.number_input("最大値", value=10.0, step=0.01)
            f_size = st.number_input("太さを入力", value = 3.0, min_value = 0.0, step = 0.5)
        with col3:
            slice = st.number_input("分割数を入力(滑らかさ)", value = 100, min_value = 0, step = 1)
            f_legend = st.text_input("凡例名を入力")
        
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

    class advancetick:  # クラスにする必要はあるのか？
        ticksetting = False
        xmajor_size=ymajor_size=xminor_size=yminor_size=xmajor_width=ymajor_width=xminor_width=yminor_width = 0
    
    a = advancetick()

    setfont = st.checkbox("フォントを指定する(軸ラベルのみ)", value = False)
    if setfont:
        fontpath = st.text_input("フォントファイルのパスを指定", placeholder = "例) C:\Windows\Fonts\HGRPP1.ttc")
        if fontpath:
            fp = FontProperties(fname=fontpath, size=fontsize)
        st.caption("システムフォントの場所 C:\\Windows\\Fonts ユーザーフォントの場所 C:\\Users\\ユーザー名\\AppData\\Local\\Microsoft\\Windows\\Fonts")
    
    a.ticksetting = st.checkbox("目盛り線の設定", value=False)
    if a.ticksetting:
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


    if function or setfont or a.ticksetting:
        if uploaded_file:
            #st.write(a.ticksetting)
            fig = plot(dpi, width, height, toptick, bottomtick, lefttick, righttick, xtickdir, ytickdir, property, legends, ja_legends, minorticks, grid, xlog, ylog, xmin, xmax, ymin, ymax, xscale, yscale, fontsize, xlabel, ylabel, fp, column, xaxis, xtick_list_num, xtick_list, ytick_list_num, ytick_list, a.ticksetting, a.xmajor_size, a.ymajor_size, a.xminor_size, a.yminor_size, a.xmajor_width, a.ymajor_width, a.xminor_width, a.yminor_width)
            if function and f and f_max > f_min:
                plt.plot(x, y, c = f_color, linewidth = f_size, label = f_legend)
            try:
                st.pyplot(fig)
                # 保存
                plt.savefig(title + expantion, bbox_inches="tight")
                # ダウンロード
                with open(title + expantion, "rb") as file:
                    btn = st.download_button(
                        label = "画像を保存",
                        data = file,
                        file_name = title + expantion,
                        key=1
                        )
            except:
                st.error("フォントファイルのパスを正しく入力できているか確認してください", icon="🚨")
    

with tab3:
    st.subheader("使い方")

with tab4:
    st.subheader("その他")