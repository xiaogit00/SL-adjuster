        '''
        FIRST MO/SL:
        MO - 100
        SL - 95
        trailing_value: (MO_actual_entry_price - last_low) * trailing_percentage : (100-95) *0.7 = 3.5
        next_stoploss_price = last_low + trailing_value : 95+ 3.5 = 98.5
        trailing_price: actual_entry_price + trailing_value = 103.5

        NEW SL:
        Candle price: 103.5
        current_stop_loss: 98.5
        trailing_value = 3.5
        next_stoploss_price = 98.5+3.5 = 102
        trailing_price = 103.5+3.5 = 107

        Listener -> gets NEW SL -> 
        '''