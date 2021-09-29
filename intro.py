import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import norm
import streamlit as st

def app():
    
    st.header("Option spread selection")
    
    mu = 200
    sigma = 20
    sigma2 = 35


    x1 = mu - 4* sigma    
    x2 = mu + 4* sigma


    z1 = ( mu - sigma ) 
    z2 = ( mu + sigma ) 

    x = np.arange(z1, z2, 0.001) # range of x in spec
    x_all = np.arange(x1, x2, 0.001) # entire range of x, both in and out of spec
    # mean = 0, stddev = 1, since Z-transform was calculated
    y = norm.pdf(x,mu,sigma)
    y_all = norm.pdf(x_all, mu, sigma)
    y2_all = norm.pdf(x_all, mu, sigma2)


    #build the plot
    fig, ax = plt.subplots(figsize=(12,8))
    plt.style.use('seaborn')
    #plt.style.use('fivethirtyeight')
    ax.plot(x_all, y2_all, c='r', linestyle='--', label='higher volatility')
    ax.plot(x_all,y_all, c='blue', label='Lower volatility')
    ax.legend(fontsize='large')


    ax.fill_between(x,y,0, alpha=0.3, color='b')
    ax.fill_between(x_all,y_all,0, alpha=0.1)
    #ax.set_xlim([-4,4])
    ax.set_xlabel('Price range ($)')
    #ax.set_yticklabels([])
    ax.set_title('IV Environment', fontdict = {'fontsize' : 20})

    plt.axvline(x=mu, c='k')
    plt.axvline(x=mu+sigma2, c='r', linestyle='--')
    plt.axvline(x=mu-sigma2, c='r', linestyle='--')
    plt.axvline(x=mu+sigma, c='blue')
    plt.axvline(x=mu-sigma, c='blue')

    ## debit spread arrow
    ax.arrow(mu+sigma, 0.65*max(y_all), -0.9*(sigma-sigma2), 0, width=0.01*max(y_all), color="k", 
                length_includes_head=True,
                head_length=abs(sigma-sigma2)/7, overhang=0.008)
    ax.arrow(mu-sigma, 0.65*max(y_all), 0.9*(sigma-sigma2), 0, width=0.01*max(y_all), color="k", 
                length_includes_head=True,
                head_length=abs(sigma-sigma2)/7, overhang=0.008)

    ## credit spread arrow
    ax.arrow(mu+sigma2, 0.25*max(y_all), 0.9*(sigma-sigma2), 0, width=0.01*max(y_all), color="k", 
                length_includes_head=True,
                head_length=abs(sigma-sigma2)/7, overhang=0.008)
    ax.arrow(mu-sigma2, 0.25*max(y_all), -0.9*(sigma-sigma2), 0, width=0.01*max(y_all), color="k", 
                length_includes_head=True,
                head_length=abs(sigma-sigma2)/7, overhang=0.008)
    y_text = 0.00
    epsilon = 0.05 * sigma
    plt.text(mu, y_text - 0.05 * max(y_all), str(mu))
    plt.text(mu+sigma, y_text - 0.05 * max(y_all), str(mu+sigma))
    plt.text(mu-sigma, y_text - 0.05 * max(y_all), str(mu-sigma))
    if sigma != sigma2:
        plt.text(mu+sigma2, y_text , str(mu+sigma2))
        plt.text(mu-sigma2, y_text , str(mu-sigma2))
    plt.text(mu-3*sigma, 0.5 *max(y_all), 'PUT side', rotation=90)
    plt.text(mu+3*sigma, 0.5* max(y_all), 'CALL side', rotation=90)
    x_width = 0.8 * sigma
    y_width = 0.1 * max(y_all)

    ## draw credit spread
    credit_spread_anchor_bearish = mu+sigma2+epsilon
    credit_spread_anchor_bullish = mu-sigma2-x_width-epsilon
    ax.add_patch( Rectangle(( credit_spread_anchor_bearish , 0.1 * max(y_all)),
                            x_width, y_width,
                            fc ='r', 
                            ec ='r',
                            lw = 2, 
                            alpha=0.4) )
    plt.text(credit_spread_anchor_bearish, 0.1 *max(y_all), ' sell \n\n\n buy', rotation=90)
    plt.text(credit_spread_anchor_bearish, 0.2 *max(y_all), 'credit spread \nBearish bias')
    ax.add_patch( Rectangle((credit_spread_anchor_bullish , 0.1 * max(y_all)),
                            x_width, y_width,
                            fc ='r', 
                            ec ='r',
                            lw = 2,
                            alpha=0.4) )
    plt.text(credit_spread_anchor_bullish, 0.1 *max(y_all), ' buy \n\n\n sell', rotation=90)
    plt.text(credit_spread_anchor_bullish, 0.2 *max(y_all), 'credit spread \nBullish bias')

    ## debit spread
    debit_spread_anchor_bullish = mu+sigma-x_width-epsilon
    debit_spread_anchor_bearish = mu-sigma+epsilon
    ax.add_patch( Rectangle(( debit_spread_anchor_bullish , 0.5 * max(y_all)),
                            x_width, y_width,
                            fc ='g', 
                            ec ='g',
                            lw = 2, 
                            alpha=0.4) )
    plt.text(debit_spread_anchor_bullish, 0.5 *max(y_all), ' buy \n\n\n sell', rotation=90)
    plt.text(debit_spread_anchor_bullish, 0.6 *max(y_all), 'debit spread \nBullish bias')
    ax.add_patch( Rectangle((debit_spread_anchor_bearish , 0.5 * max(y_all)),
                            x_width, y_width,
                            fc ='g', 
                            ec ='g',
                            lw = 2,
                            alpha=0.4) )
    plt.text(debit_spread_anchor_bearish, 0.5 *max(y_all), ' sell \n\n\n buy', rotation=90)
    plt.text(debit_spread_anchor_bearish, 0.6 *max(y_all), 'debit spread \nBearish bias')

    savefigure = st.sidebar.checkbox("Save figure")
    if savefigure:
        plt.savefig('normal_curve.png', dpi=200, bbox_inches='tight')

    st.pyplot(fig)


    st.markdown('''
    When IV is lower, it can make credit spreads less expensive and deliver smaller potential profits 
    and larger potential losses compared to verticals at the same strike price when IV is higher. 
    When the IV percentile is lower than 50%, that’s when you might consider debit spreads instead.

    So, when the IV percentile is, say, above 50%, you might select trades by looking at credit spreads—short put spreads if you’re bullish; short call spreads if you’re bearish. 
    When the IV percentile is under 50%, you might select trades by looking at debit spreads—long call spreads if you’re bullish; long put spreads if you’re bearish.
    ''')


