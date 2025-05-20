def predict_rub_salary(payment_from, payment_to):      
    if payment_from and payment_to:
        return int((payment_from+payment_to)/2)
    elif payment_to:
        return int(payment_to*0.8)
    else:
        return int(payment_from*1.2)