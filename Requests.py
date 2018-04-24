#The functions in the class would return the requests spicified by the users.
class Request():
    def Pong():
        return json.dumps({'e':'pong'})
    def Ticker(crypto,money='USD'):
        return json.dumps({'e':'ticker','data':[crypto,money]})
    def Get_Balance():
        return json.dumps({'e':'get-baclance'})
    def Order_Book(crypto,money='USD',subscribe=False,depth=-1):
        return json.dumps({
                            'e':'order-book-subscribe',
                            'data':{
                                    'pair':[crypto,money],'subscribe':subscribe,'depth':depth
                                        }
                            })
    def Cancel_Order_Book(crypto,money='USD'):
        return json.dumps({
                            'e':'order-book-unsubscribe',
                            'data':{
                                    'pair':[crypto,money]
                                        }
                            })
    
    def Place_Order(crypto,amount,price,type,money='USD'):
        return json.dumps({
                            'e':'place-order',
                            'data':{
                                    'pair':[crypto,money],'amount':amount,'price':str(price),'type':type
                                        }
                            })
    
    def Cancel_Place_Order(id):
        return json.dumps({
                            'e':'cancel-order',
                            'data':{
                                    'order_id':id
                                    }
                            })