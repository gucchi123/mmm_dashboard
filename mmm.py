import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    link = '[元データとその他の分析結果の確認](https://github.com/gucchi123/mmm_data)'

    dolists = ["モデルの正確性確認", "広告チャネルの金額確認"]
    DoList = st.sidebar.selectbox(
        '確認したい事項を選択：',dolists
    )


    if DoList == "モデルの正確性確認":
        st.header('＜東京男性＞過去データモデルの適合度')
        st.markdown(link, unsafe_allow_html=True)   
        st.image("https://raw.githubusercontent.com/gucchi123/mmm_data/main/5_1733_1.png")


    elif DoList == "広告チャネルの金額確認":
        st.header('＜東京男性＞広告最適化ダッシュボード')
        
        st.markdown(link, unsafe_allow_html=True)
        channels = ["シミュレート結果一覧","Facebook広告", "Google広告", "Influencer固定報酬", "Offline施策", "Yahoo広告", "Twitter広告"]
        selected_channel = st.sidebar.selectbox(
        '広告チャネルを選択：',channels)
        training_data_path = r"batch491-1186.csv"
        optimized_file = r"5_1724_3_reallocated.csv" 
        
        df_training = pd.read_csv(training_data_path, encoding="cp932")
        

        def investment(channel, file, data):
            result_data = pd.read_csv(file, encoding="CP932")
            selected = result_data.loc[result_data.loc[:,"channels"]==channel,:]
            st.subheader("広告項目：{}".format(channel))
            fig = plt.figure(figsize=(6,3))
            plt.title("Spend for {} per day".format(channel))
            plt.vlines(selected.loc[:, "initSpendUnit"], 0, 50, "0.3", linestyles='dashed', label="Current Ave")
            plt.vlines(selected.loc[:, "optmSpendUnit"], 0, 50, "red", linestyles='dashed', label="Optm Ave")
            st.write("＜1日あたりの{}消化金額サマリー＞".format(channel))
            
            names = ["現状投資額(Current Ave)","最適値投資額(Optm Ave)", "広告投資金額差分", "CPA改善差分"]
            num_columns = len(names)
            cols = st.columns(num_columns)
            for name, col in zip(names, cols):
                if name == names[0]:
                    #value = selected.loc[:, "initSpendUnit"].iloc[-1]
                    #col.metric(label=name, value=f'{value:,.3f} 円')
                    try:
                        value = selected.loc[:, "initSpendUnit"].iloc[-1]
                        col.metric(label=name, value=f'{value:,.3f} 円')
                    except IndexError:
                        value = data.loc[ data.loc[:, channel]>0 ,channel].mean()
                        col.metric(label=name, value=f'{value:,.3f} 円')
                        
                if name == names[1]:
                    try:
                        value = selected.loc[:, "optmSpendUnit"].iloc[-1]
                        col.metric(label=name, value=f'{value:,.3f} 円')
                    except:
                        value = 0
                        col.metric(label=name, value=f'{value:,.3f} 円')
                if name == names[2]:
                    try:
                        value = 0 - data.loc[ data.loc[:, channel]>0 ,channel].mean()
                        col.metric(label=name, value=f'{value:,.3f} 円')
                    except:
                        value = 0
                        col.metric(label=name, value=f'{value:,.3f} 円')
                if name == names[3]:
                    try:
                        value = selected.loc[:, "optmResponseUnitLift"].iloc[-1]
                        col.metric(label=name, value=f'{value:,.3f} 円')
                    except:
                        value = 0
                        col.metric(label=name, value=f'{value:,.3f} 円')         

            
            #st.write(data.loc[ data.loc[:, channel]>0 ,channel])
            st.write('')
            plt.hist(data.loc[ data.loc[:, channel]>0 ,channel], bins=6, color="0.8")
            plt.legend()
            st.write("＜グラフ：過去の平均消費金額と最適化＞")
            st.pyplot(fig)
            st.write('')
            st.write('-----------------------------------------------------------------------')
            
        if selected_channel == "シミュレート結果一覧":
            st.image("https://raw.githubusercontent.com/gucchi123/mmm_data/main/5_1724_3_reallocated_hist.png")
        
        if selected_channel == "Facebook広告":
            selected_channels = [ i for i in df_training.columns if "FB" in i if "_S" in i]
            #st.write(selected_channels)
            for channel in selected_channels:
                #st.write(channel)
                investment(channel, optimized_file, df_training)

        if selected_channel == "Google広告":
            selected_channels = [ i for i in df_training.columns if "Google" in i if "_S" in i]
            #st.write(selected_channels)
            for channel in selected_channels:
                #st.write(channel)
                investment(channel, optimized_file, df_training)

        if selected_channel == "Influencer固定報酬":
            selected_channels = [ i for i in df_training.columns if "Influencer" in i if "_S" in i]
            #st.write(df_training.columns)
            for channel in selected_channels:
                #st.write(channel)
                investment(channel, optimized_file, df_training)

        if selected_channel == "Yahoo広告":
            selected_channels = [ i for i in df_training.columns if "Yahoo" in i if "_S" in i]
            #st.write(selected_channels)
            for channel in selected_channels:
                #st.write(channel)
                investment(channel, optimized_file, df_training)

        if selected_channel == "Twitter広告":
            selected_channels = [ i for i in df_training.columns if "Twitter" in i if "_S" in i]
            #st.write(selected_channels)
            for channel in selected_channels:
                #st.write(channel)
                investment(channel, optimized_file, df_training)


        if selected_channel == "Offline施策":
            selected_channels = [ i for i in df_training.columns if "boolean" in i if "_S" in i]
            #st.write(selected_channels)
            for channel in selected_channels:
                #st.write(channel)
                investment(channel, optimized_file, df_training)

if __name__ == '__main__':
    main()