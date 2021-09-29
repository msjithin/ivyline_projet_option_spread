import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def spread_plot(current_price, strike_price1, strike_price2, type='debit'):
    fig, ax = plt.subplots(figsize=(4,3))
    plt.style.use('seaborn')
    mu = current_price
    sigma = 0.2 * mu
    dominant_side = ''

    if (strike_price1 < current_price and strike_price2<current_price ):
        dominant_side = 'PUT'
        x1 = mu - 2*sigma
        x2 = mu + sigma
    elif (strike_price1 > current_price and strike_price2>current_price ):
        dominant_side = 'CALL'
        x1 = mu -  sigma    
        x2 = mu + 2* sigma
    else:
        x1 = mu - 3*sigma
        x2 = mu + 3*sigma

    x_all = np.arange(x1, x2, 0.001) # entire range of x, both in and out of spec
    y_all = norm.pdf(x_all, mu, sigma)
    ax.plot(x_all,y_all, c='blue')
    plt.axvline(x=mu, c='k')
    plt.axvline(x=strike_price1, c='g', linestyle='--')
    plt.axvline(x=strike_price2, c='r', linestyle='--')
    plt.text(strike_price1, 0, str(strike_price1), rotation=90)
    plt.text(strike_price2, 0.2*max(y_all), str(strike_price2), rotation=90)
    if dominant_side == 'PUT':
        plt.text(mu-2*sigma, 0.5 *max(y_all), 'PUT side', rotation=90)
    elif dominant_side == 'CALL':
        plt.text(mu+2*sigma, 0.5* max(y_all), 'CALL side', rotation=90)
    else:
        plt.text(mu-2*sigma, 0.5 *max(y_all), 'PUT side', rotation=90)
        plt.text(mu+2*sigma, 0.5* max(y_all), 'CALL side', rotation=90)
    return fig