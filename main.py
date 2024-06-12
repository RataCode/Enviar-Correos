from clases.daychanger import changeDay

if __name__== '__main__':
    try:
        cd = changeDay()
        cd.getDays()
        cd.changeNotification()
        cd.sendMail()
        cd.changeDate()
        print()
    except ValueError as err:
        print(err)