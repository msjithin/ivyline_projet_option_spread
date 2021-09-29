import streamlit as st
from spread_plot import spread_plot
import option_class 

def app():
    st.title('**DEBIT SPREAD**')
    current_price = float(st.text_input("Current Price", 173))
    spread_type = ''
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("Buy Strike price")
    buy_price = float(col2.text_input("Buy", 177.50))
    col3.markdown("Sell Strike price")
    sell_price = float(col4.text_input("Sell", 180))    
    buyoption_price = float(col2.text_input("Bid", 1.52))
    selloption_price = float(col4.text_input("Ask", 0.91))
    col1.markdown("")
    col1.markdown("")
    col1.markdown("")
    col3.markdown("")
    col3.markdown("")
    col3.markdown("")
    col1.markdown("Buy option price (Bid)")
    col3.markdown("Sell option price (Ask)")
    cost = round(abs(buyoption_price-selloption_price), 2)
    max_profit = round(abs(buy_price-sell_price) - cost, 2)
    max_loss   = cost
    if current_price>buy_price and current_price>sell_price:
        spread_type = 'PUT'
    else:
        spread_type = 'CALL'
    if spread_type == 'PUT':
        breakeven_price = buy_price - cost
    else:
        breakeven_price = buy_price + cost
    probability = 68
    st.markdown(''' This is a debit **{}** spread '''.format(spread_type))
    col_fig,col_text = st.columns([3,1])
    col_fig.pyplot(spread_plot(current_price, buy_price, sell_price, 'debit'))

    col_text.markdown('''
    Cost:  $ {} \n
    Max Profit: $ {} per share \n
    Max Loss Potential: $ {} \n 
    Breakeven Price: $ {} \n 
    Probability of Finishing OTM:   1 - Delta
    '''.format(cost, max_profit, max_loss, breakeven_price))
    
    st.markdown("## Analysis")
    if spread_type == 'CALL':
        st.markdown(f'''
        Cost =  {buyoption_price} – {selloption_price} = {cost} \n
        Max Profit: {sell_price} - {buy_price} - {cost} = {max_profit} \n
        Max loss : {max_loss}  = cost \n 
        Breakeven price = {buy_price} + {cost} = {breakeven_price} \n
        ''')
    else:
        st.markdown(f'''
        Cost =  {buyoption_price} – {selloption_price} = {cost} \n
        Max Profit: {buy_price} - {sell_price} - {cost} = {max_profit}\n
        Max loss : {max_loss}  = cost \n
        Breakeven price = {buy_price} - {cost} = {breakeven_price} \n
        ''')
    # st.markdown("**Payoff diagram**")
    # payoffcol1, payoffcol2 = st.columns([3,1])
    # payoffcol1.pyplot(payoff(current_price, buy_price, sell_price, 'debit'))
    range_xaxis = abs(sell_price-buy_price)*2
    if spread_type == 'CALL':
        obj = option_class.OptionStrat('Bull Call Spread', current_price, start=breakeven_price-range_xaxis, stop=breakeven_price+range_xaxis)
        obj.short_call(sell_price, selloption_price)
        obj.long_call(buy_price, buyoption_price)
        st.pyplot(obj.plot(color='black'))
        st.markdown('  \n '.join(obj.describe()))
    if spread_type == 'PUT':
        obj = option_class.OptionStrat('Bear Put Spread', current_price, start=breakeven_price-range_xaxis, stop=breakeven_price+range_xaxis)
        obj.short_put(sell_price, selloption_price)
        obj.long_put(buy_price, buyoption_price)
        st.pyplot(obj.plot(color='black'))
        st.markdown('  \n '.join(obj.describe()))