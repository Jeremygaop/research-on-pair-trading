import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression


def test_OLS(data, factors, start_date, train_period, test_period):
    all_r2_in = []
    all_r2_out = []
    all_rmse_in = []
    all_rmse_out = []
    all_hit_ratio_in = []
    all_hit_ratio_out = []

    start_date = start_date

    while start_date <= data.index[-1]:
        train_date = valid_date_n_days_later(start_date, data, train_period)
        if not train_date:
            break
        test_date = valid_date_n_days_later(train_date, data, 1)
        if not test_date:
            break
        end_date = valid_date_n_days_later(test_date, data, test_period)
        if not end_date:
            break

        train_data = data.loc[start_date:train_date]
        train_data = train_data[:-1]
        test_data = data.loc[test_date:end_date]
        test_data = test_data[:-1]

        X_train = train_data[factors]
        y_train = train_data['delta_1']

        X_test = test_data[factors]
        y_test = test_data['delta_1']

        # fit the OLS
        model_ols = LinearRegression()
        model_ols.fit(X_train, y_train)

        y_train_pred = model_ols.predict(X_train)
        y_test_pred = model_ols.predict(X_test)

        r2_in = model_ols.score(X_train, y_train)
        r2_out = model_ols.score(X_test, y_test)
        rmse_in = np.sqrt(np.mean((model_ols.predict(X_train) - y_train) ** 2))
        rmse_out = np.sqrt(np.mean((model_ols.predict(X_test) - y_test) ** 2))

        # calculate hit ratio
        hit_ratio_in = 0
        hit_ratio_out = 0
        for i in range(len(y_train_pred)):
            if y_train_pred[i] * y_train[i] > 0:
                hit_ratio_in += 1

        for i in range(len(y_test_pred)):
            if y_test_pred[i] * y_test[i] > 0:
                hit_ratio_out += 1

        # add the result to the list
        all_r2_in.append(r2_in)
        all_r2_out.append(r2_out)
        all_rmse_in.append(rmse_in)
        all_rmse_out.append(rmse_out)
        all_hit_ratio_in.append(hit_ratio_in / len(y_train_pred))
        all_hit_ratio_out.append(hit_ratio_out / len(y_test_pred))

        start_date = valid_date_n_days_later(start_date, data, 1)

    # plot the 4 lists in the same plot
    plt.plot(all_r2_in, label='in-sample R2')
    plt.plot(all_r2_out, label='out-sample R2')
    plt.plot(all_rmse_in, label='in-sample RMSE')
    plt.plot(all_rmse_out, label='out-sample RMSE')
    plt.plot(all_hit_ratio_in, label='in-sample hit ratio')
    plt.plot(all_hit_ratio_out, label='out-sample hit ratio')
    plt.title('OLS')
    plt.legend()
    plt.show()

    # print R2
    print("in-sample R2: ", sum(all_r2_in) / len(all_r2_in))
    print("out-sample R2: ", sum(all_r2_out) / len(all_r2_out))
    print("in-sample RMSE: ", sum(all_rmse_in) / len(all_rmse_in))
    print("out-sample RMSE: ", sum(all_rmse_out) / len(all_rmse_out))
    print("in-sample hit ratio: ", sum(all_hit_ratio_in) / len(all_hit_ratio_in))
    print("out-sample hit ratio: ", sum(all_hit_ratio_out) / len(all_hit_ratio_out))


def test_logistic(data, factors, start_date, train_period, test_period, symbol, filter_factor='RSI', upper_quantile=0.5,
                  lower_quantile=0.5):
    all_r2_in = []
    all_r2_out = []
    all_rmse_in = []
    all_rmse_out = []
    all_hit_ratio_in = []
    all_hit_ratio_out = []
    y_test_preds = pd.Series()

    start_date = start_date

    while start_date <= data.index[-1]:
        train_date = valid_date_n_days_later(start_date, data, train_period)
        if not train_date:
            break
        test_date = valid_date_n_days_later(train_date, data, 1)
        if not test_date:
            break
        end_date = valid_date_n_days_later(test_date, data, test_period)
        if not end_date:
            break

        train_data = data.loc[start_date:train_date]
        train_data = train_data[:-1]

        filtor_upper = train_data[filter_factor].quantile(upper_quantile)
        filtor_lower = train_data[filter_factor].quantile(lower_quantile)


        test_data = data.loc[test_date:end_date]
        # select the data with spread which is lager than the upper quantile or lower than the lower quantile
        test_data = test_data[(test_data[filter_factor] > filtor_upper) | (test_data[filter_factor] < filtor_lower)]
        test_data = test_data[:-1]

        if len(test_data) == 0:
            start_date = valid_date_n_days_later(start_date, data, 1)
            continue

        X_train = train_data[factors]
        y_train = train_data['delta_1']

        # convert y_train to binary
        y_train = y_train.apply(lambda x: 1 if x > 0 else -1)

        X_test = test_data[factors]
        y_test = test_data['delta_1']
        # convert y_test to binary
        y_test = y_test.apply(lambda x: 1 if x > 0 else -1)

        # fit the logistic regression
        model_logistic = LogisticRegression()
        model_logistic.fit(X_train, y_train)

        y_train_pred = model_logistic.predict(X_train)
        y_test_pred = model_logistic.predict(X_test)
        y_test_pred = pd.Series(y_test_pred, index=y_test.index)
        y_test_preds = pd.concat([y_test_preds, y_test_pred], axis=0)

        r2_in = model_logistic.score(X_train, y_train)
        r2_out = model_logistic.score(X_test, y_test)
        rmse_in = np.sqrt(np.mean((model_logistic.predict(X_train) - y_train) ** 2))
        rmse_out = np.sqrt(np.mean((model_logistic.predict(X_test) - y_test) ** 2))


        # calculate hit ratio
        hit_ratio_in = 0
        hit_ratio_out = 0
        for i in range(len(y_train_pred)):
            if y_train_pred[i] * y_train[i] > 0:
                hit_ratio_in += 1

        for i in range(len(y_test_pred)):
            if y_test_pred[i] * y_test[i] > 0:
                hit_ratio_out += 1

        # add the result to the list
        all_r2_in.append(r2_in)
        all_r2_out.append(r2_out)
        all_rmse_in.append(rmse_in)
        all_rmse_out.append(rmse_out)
        all_hit_ratio_in.append(hit_ratio_in / len(y_train_pred))
        all_hit_ratio_out.append(hit_ratio_out / len(y_test_pred))

        start_date = valid_date_n_days_later(start_date, data, 1)

    # # plot the 4 lists in the same plot
    # plt.plot(all_r2_in, label='in-sample R2')
    # plt.plot(all_r2_out, label='out-sample R2')
    # # plt.plot(all_rmse_in, label='in-sample RMSE')
    # # plt.plot(all_rmse_out, label='out-sample RMSE')
    # plt.plot(all_hit_ratio_in, label='in-sample hit ratio')
    # plt.plot(all_hit_ratio_out, label='out-sample hit ratio')
    # plt.title('Logistic Regression on ' + symbol)
    # plt.legend()
    # plt.show()
    #
    # # print R2
    # print("in-sample R2: ", sum(all_r2_in) / len(all_r2_in))
    # print("out-sample R2: ", sum(all_r2_out) / len(all_r2_out))
    # print("in-sample RMSE: ", sum(all_rmse_in) / len(all_rmse_in))
    # print("out-sample RMSE: ", sum(all_rmse_out) / len(all_rmse_out))
    # print("in-sample hit ratio: ", sum(all_hit_ratio_in) / len(all_hit_ratio_in))
    # print("out-sample hit ratio: ", sum(all_hit_ratio_out) / len(all_hit_ratio_out))

    # set the name of y_test_preds as signal
    y_test_preds = pd.DataFrame(y_test_preds, columns=['signal'])

    data = pd.merge(data, y_test_preds, left_index=True, right_index=True, how='left')

    data = data[['spread', 'signal']]
    return data


def valid_date_n_days_later(start, all_data, n):
    i = 1
    while i <= n:
        start = start + pd.DateOffset(days=1)
        if start in all_data.index:
            i = i + 1
        if start > all_data.index[-1]:
            return False
    return start
