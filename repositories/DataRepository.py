from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

#---------------------------------------------------------------------------

    @staticmethod
    def create_sensor(Naam,Beschrijving,Aankoopprijs,Type,Eenheid):
        sql='INSERT INTO Sensor (Naam,Beschrijving,Aankoopprijs,Type,Eenheid) VALUES (%s,%s,%s,%s,%s)'
        parameters = [Naam,Beschrijving,Aankoopprijs,Type,Eenheid]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def update_sensor(Naam,Beschrijving,Aankoopprijs,Type,Eenheid,SensorID):
        sql=("UPDATE Sensor set Naam = %s, Beschrijving = %s, Aankoopprijs = %s, Type = %s, Eenheid = %s  WHERE SensorID = %s")
        parameters= [Naam,Beschrijving,Aankoopprijs,Type,Eenheid,SensorID]
        return Database.execute_sql(sql, parameters)
    
    @staticmethod
    def create_actuator(Naam,Merk,Beschrijving,Aankoopprijs,Type,Eenheid):
        sql='INSERT INTO Actuator (Naam,Beschrijving,Aankoopprijs,Type,Eenheid) VALUES (%s,%s,%s,%s,%s)'
        parameters = [Naam,Beschrijving,Aankoopprijs,Type,Eenheid]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def update_actuator(Naam,Beschrijving,Aankoopprijs,Type,Eenheid,ActuatorID):
        sql=("UPDATE Actuator set Naam = %s, Beschrijving = %s, Aankoopprijs = %s, Type = %s, Eenheid = %s  WHERE SensorID = %s")
        parameters= [Naam,Beschrijving,Aankoopprijs,Type,Eenheid,ActuatorID]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def create_meting(SensorID, ActuatorID, Datum,Waarde,Toestand,Commentaar):
        sql='INSERT INTO Metingen (SensorID, ActuatorID,Datum,Waarde,Toestand,Commentaar) VALUES (%s,%s,%s,%s,%s,%s)'
        parameters = [SensorID, ActuatorID,Datum,Waarde,Toestand,Commentaar]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def update_meting(SensorID, ActuatorID, Datum,Waarde,Toestand,Commentaar, MeetwaardeID):
        sql=("UPDATE Metingen set SensorID = %s, ActuatorID = %s, Datum = %s, waarde = %s, Toestand = %s, Commentaar = %s  WHERE MeetwaardeID = %s")
        parameters= [SensorID, ActuatorID, Datum,Waarde,Toestand,Commentaar,MeetwaardeID]
        return Database.execute_sql(sql, parameters)


