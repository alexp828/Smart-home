import nexmo

def send_SMS(nexmo_obj, phone_num):
    nexmo_obj.send_message({
        'from': phone_num,
        'to': phone_num,
        'text': 'testing',
    })


if __name__ == '__main__':
    client_nexmo = nexmo.Sms(key='9768791e', secret='LQF3kbL6grfKJq5o')
    phone_num = '6502292666'
    send_SMS(client_nexmo, phone_num)
