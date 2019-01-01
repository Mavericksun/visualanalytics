# pylint: disable=E1101, C0111, C0103

import matplotlib
matplotlib.use('Agg')

from UTCDAL.Utilities.DataAccess import getdata_wc as webctrl
# from UTCDAL.Design.TimeseriesAnalysis import generate_features
from UTCDAL.Design.TimeseriesAnalysis import TSAnalysis
from UTCDAL.Externals import pd, plt, time, datetime, pickle
plt.style.use('seaborn-muted')
import matplotlib.dates as mdates
# import ipdb
import os


def main():
    initialize()
    # with open('cache_DATA.pkl', 'wb') as f:
    #     pickle.dump(DATA, f)
    while True:
        update_data()
        plot_energy_curves()
        time.sleep(60)

def initialize():
    # retrieve last 14 days data, and calculate classifications
    print('initialization start')
    today = (datetime.datetime.now() - datetime.timedelta(days=0, hours=5))
    today_str = today.strftime('%Y-%m-%d')
    day_14_before = today - datetime.timedelta(days=7)

    df_last2weeks = webctrl.get_trend(GQL, day_14_before.strftime('%Y-%m-%d'), '7')

    sf_status = {'KNN': [], 'SVM': [], 'RF': []}
    sf_index = []
    for i in range(7):
        date = (day_14_before + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        df_date = df_last2weeks.loc[date, :]
        DATA[date] = df_date
        pred_knn, pred_svm, pred_rf = predict_single_day(df_date)
        sf_status['KNN'].append(pred_knn)
        sf_status['SVM'].append(pred_svm)
        sf_status['RF'].append(pred_rf)
        sf_index.append(date)
    DATA['sf_status'] = pd.DataFrame(sf_status, index=sf_index)
    print('7 days data retriving completed')
    
    # retrieve today's data
    df_today = webctrl.get_trend(GQL, today_str, '1').sort_index(ascending=True)
    DATA['today'] = df_today
	
    print('initialization completed')

def update_data():
    # TODO: automatically calculate the time based on time zone
    today = (datetime.datetime.now() - datetime.timedelta(days=0, hours=5)).strftime('%Y-%m-%d')
    # print(f'Today: {today}.')
    df_today = webctrl.get_trend('#utrc_l_meter_13/real_pwr_tn', today, '1')
    DATA['today'] = df_today
    print(df_today.head())

    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1, hours=5)).strftime('%Y-%m-%d')
    if yesterday not in DATA.keys():
        print('Entered a new day. Now updating yesterday\'s data...')
        df_yesterday = webctrl.get_trend('#utrc_l_meter_13/real_pwr_tn', yesterday, '1')
        DATA['yesterday'] = df_yesterday
        DATA[yesterday] = df_yesterday
        pred_knn, pred_svm, pred_rf = predict_single_day(df_yesterday)
        DATA['sf_status'].loc[yesterday, ['KNN', 'SVM', 'RF']] = [pred_knn, pred_svm, pred_rf]
        day_14_before = (datetime.datetime.strptime(today, '%Y-%m-%d') - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        del DATA[day_14_before]
        print('Updating the figure for last 2 weeks...')
    plot_last_14_days()
    print('update completed')

def plot_energy_curves():
    # yesterday = '2017-09-17'; today = '2017-09-18'
    today = (datetime.datetime.now() - datetime.timedelta(days=0, hours=5)).strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1, hours=5)).strftime('%Y-%m-%d')

    df_yesterday = DATA[yesterday]
    df_today = DATA['today']

    # pred_knn, pred_svm, pred_rf = DATA['sf_status'].loc[yesterday, :].values
    # print('Predictions:', pred_knn, pred_svm, pred_rf)

    _, axes = plt.subplots(1, 2, figsize=(12, 1.5), sharey=True)
    df_yesterday_index = df_yesterday.index.to_pydatetime()  #[x for x in df_yesterday.index]
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>',type(df_today.index))
    # ipdb.set_trace()
    df_today_index = df_today.index.to_pydatetime()  # [x for x in df_today.index]
    
    axes[0].plot(df_yesterday_index, df_yesterday['values'])
    axes[1].plot(df_today_index, df_today['values'])
    # axes[0].set_title(yesterday + '  knn: {} / svm: {} / rf: {}'.format(pred_knn, pred_svm, pred_rf))
    axes[1].set_title(today)
    axes[0].set_xlim(datetime.datetime.strptime(yesterday + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                     datetime.datetime.strptime(yesterday + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    axes[1].set_xlim(datetime.datetime.strptime(today + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                     datetime.datetime.strptime(today + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    for ax in axes:
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axes[0].set_ylabel('Power (kW)')
    for ax in axes:
        ax.grid(True, ls='dotted', which='both')
        ax.set_xlabel('')
        for tick in ax.xaxis.get_major_ticks(): tick.label.set_fontsize(8)
        for tick in ax.xaxis.get_minor_ticks(): tick.label.set_fontsize(8)

    plt.savefig('static/energy.svg', bbox_inches='tight')
    plt.close()

def plot_last_14_days():
    sf_status = pd.DataFrame(DATA['sf_status'].copy())

    fig, ax = plt.subplots(figsize=(9, 2))
    for i, day in enumerate(sf_status.index):
        ax.fill_between([i-0.45, i+0.45], [0, 0], [0.92, 0.92], color=COLORS[sf_status.loc[day, 'KNN']])
        ax.fill_between([i-0.45, i+0.45], [1, 1], [1.92, 1.92], color=COLORS[sf_status.loc[day, 'SVM']])
        ax.fill_between([i-0.45, i+0.45], [2, 2], [2.92, 2.92], color=COLORS[sf_status.loc[day, 'RF']])
    ax.set_xlim(-0.45, sf_status.shape[0]-1+0.45)
    ax.set_ylim(0, 3)
    ax.set_xticks(range(sf_status.shape[0]))
    ax.set_xticklabels([x[-5:] for x in sf_status.index])
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(['KNN', 'SVM', 'RF'])
    fig.tight_layout()
    plt.savefig('static/last14predictions.svg', bbox_inches='tight')

def predict_single_day(data):
    ts_analysis = TSAnalysis(data=data)
    ts_analysis.generate_features()
    features = ts_analysis.features
    # features = generate_features(data)
    # feature_select = selector.transform(scaler.transform(features))
    features[:] = scaler.transform(features)
    feature_select = features.loc[:, selector]
    pred_knn = clf_knn.predict(feature_select)
    pred_svm = clf_svm.predict(feature_select)
    pred_rf = clf_rf.predict(feature_select)
    return pred_knn[0], pred_svm[0], pred_rf[0]

def load_pickle(fname):
    with open(fname, 'rb') as f:
        ret = pickle.load(f)
    return ret

if __name__ == "__main__":
    # load trained models
    # selector = load_pickle('static/sf36/model_selector.pkl')
    selector = load_pickle('top_feat_name.pkl')
    scaler = load_pickle('scaler.pkl')
    clf_knn = load_pickle('model_knn.pkl')
    clf_svm = load_pickle('model_svm.pkl')
    clf_rf = load_pickle('model_rf.pkl')
    print('Load models complete.')

    DATA = {}   ## Using this as some kind of RAM database
    # DATA = load_pickle('cache_DATA.pkl')

    GQL = '#utrc_l_meter_13/real_pwr_tn'   # AHU36 SF

    with open('secret.txt', 'r') as f:
        os.environ["WEBCTRLPASS"] = f.readline().strip()
        os.environ["WEBCTRLUSER"] = f.readline().strip()
    os.environ["WEBCTRLSERVER"] = "172.31.3.16"

    COLORS = {
        'Normal': 'g',
        'daytime on': '#023474',
        'day spike': '#FFB612',
        'night on': '#FC4C02',
        'morning on': '#862633',
        'wholeday on': '#9C824A',
        'short operations': 'k',
        'wholeaday off': '#9C824A'
    }

    main()
