from librerias.lib import *

class changeDay:
    def __init__(self, **kwargs):
        super().__init__()
        self.rango = []
        self.message= None
        self.today= date.today()
        self.calendario=[]


    def getDays(self):
        # calendario = pd.DataFrame(calendar_collection.aggregate([]))   
        self.calendario=pd.DataFrame(list(calendar_collection.aggregate([{"$match":{"dato":"numero"}}]))[0]["datos"])
        ten = (self.today +timedelta(days=10)).strftime('%m-%d-%Y')
        hoy= self.today.strftime('%m-%d-%Y')
        self.calendario.Fecha=pd.to_datetime(self.calendario.Fecha.apply(lambda x: f'{x}'), format='%d-%m-%Y')
        self.rango = self.calendario[(self.calendario.Fecha >= hoy) & (self.calendario.Fecha <= ten)]
        
    def changeNotification(self):
        if len(self.rango) != 0:
            user_collection.update_many({"user_name":{"$in": users_names}}, {"$set": {"notification": True}})
        else:
            user_collection.update_many({"user_name":{"$in": users_names}}, {"$set": {"notification": False}})

    
    def sendMail(self):

        if len(self.rango)!=0:
            try:
                string = self.sendConfig()
                if string!="":
                    smtp_server = smtplib.SMTP_SSL(server, port)
                    smtp_server.ehlo()
                    smtp_server.login(sender, password)
                    smtp_server.sendmail(sender, users_names, self.message.as_string())
                    smtp_server.close()
                    print ("¡Se ha enviado correctamente!")
                    
            except Exception as ex:
                print ("Ha ocurrido un error...",ex)    

    def getstrnot(self):
        uno=""
        cinco=""
        diez=""
        ten = (self.today +timedelta(days=10)).strftime('%m-%d-%Y')
        fiv = (self.today +timedelta(days=5)).strftime('%m-%d-%Y')
        one = (self.today +timedelta(days=1)).strftime('%m-%d-%Y')
        for event in self.rango.to_dict(orient="records"):
            fechaStr= event["Fecha"].strftime("%m-%d-%Y")
            fechaform= event["Fecha"].strftime("%d-%m-%Y")
            if fechaStr==one:
                if uno=="":
                    uno="Eventos el "+fechaform+" (Falta 1 día): "
                uno+=event["Nombre"]+"-"+event["Organnumeroo"]+", "
            elif fechaStr==fiv:
                if cinco=="":
                    cinco="Eventos el "+fechaform+" (Faltan 5 días): "
                cinco+=event["Nombre"]+"-"+event["Organnumeroo"]+", "
            elif fechaStr==ten:
                if diez=="":
                    diez="Eventos el "+fechaform+" (Faltan 10 días): "
                diez+=event["Nombre"]+"-"+event["Organnumeroo"]+", "

        uno=uno[0:-2]+".<br>" if uno!="" else ""
        cinco=cinco[0:-2]+".<br>"if cinco!="" else ""
        diez=diez[0:-2]+".<br>"if diez!="" else ""
        return uno+cinco+diez

    def changeDate(self):
        one = (self.today).strftime('%m-%d-%Y')
        outOfBounds = self.calendario[self.calendario["Fecha"]<one]


        if len(outOfBounds)!=0:
            # Anual
            anual = outOfBounds[outOfBounds["Periodo"]=="Anual"].copy()
            anual["Fecha_new"]=anual["Fecha"]+pd.DateOffset(years=1)

            # Mensual
            mensual = outOfBounds[outOfBounds["Periodo"]=="Mensual"].copy()
            mensual["Fecha_new"]=mensual["Fecha"]+pd.DateOffset(months=1)

            # Trimestral
            trimestral = outOfBounds[outOfBounds["Periodo"]=="Trimestral"].copy()
            trimestral["Fecha_new"]=trimestral["Fecha"]+pd.DateOffset(months=3)

            inOfBounds=pd.concat([trimestral, anual,mensual,self.calendario])
            inOfBounds=inOfBounds[~inOfBounds.index.duplicated(keep='first')]
            inOfBounds.Fecha_new=inOfBounds.Fecha_new.fillna(inOfBounds.Fecha)
            inOfBounds.Fecha = inOfBounds.Fecha_new
            inOfBounds.drop('Fecha_new', axis=1, inplace=True)
            inOfBounds.sort_index(inplace=True)
            inOfBounds.Fecha=inOfBounds.Fecha.dt.strftime('%d-%m-%Y')

            calendar_collection.update_many({"dato":"numero"}, {"$set":{"datos":inOfBounds.to_dict(orient="records")}})



    def sendConfig(self):
        string = self.getstrnot()
        if string!="":
            self.message = MIMEMultipart("alternative")
            self.message["Subject"] = f"{str(len(self.rango))+' evento disponible.' if len(self.rango)==1 else str(len(self.rango))+' eventos disponibles.'}"
            self.message["From"] = "ATENCION <"+sender+">"
            self.message["Cco"] = ", ".join(users_names)
            
            data = dataText
            data=data.replace("TITULO","ATENCIÓN")
            data=data.replace("CUERPO",f"{string}")
            data=data.replace("BOTON","Acceder al calendario")
            body = data


            part = MIMEText(body, "html")
            self.message.attach(part)
        return string