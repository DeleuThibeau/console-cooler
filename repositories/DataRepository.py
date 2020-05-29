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
    def read_devices():
        sql="SELECT * FROM Device"
        return Database.get_rows(sql)

    @staticmethod
    def read_device(DeviceID):
        sql="SELECT * FROM Device WHERE DeviceID = %s"
        parameters=[DeviceID]
        return Database.get_one_row(sql, parameters)        

    @staticmethod
    def create_device(TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving):
        sql='INSERT INTO Device (TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving) VALUES (%s,%s,%s,%s,%s,%s)'
        parameters = [TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def update_device(TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving, DeviceID):
        sql=("UPDATE Device set TypeDevice = %s, Naam = %s, Eenheid = %s, Merk =%s, Aankoopprijs = %s, Beschrijving = %s WHERE DeviceID = %s")
        parameters= [TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving,DeviceID]
        return Database.execute_sql(sql, parameters)




    @staticmethod
    def read_metingen():
        sql="SELECT * FROM Metingen"
        return Database.get_rows(sql)


    @staticmethod
    def read_metingen_device(DeviceID):
        sql="SELECT * FROM Metingen WHERE  DeviceID = %s ORDER BY MetingID DESC Limit 1"
        parameters=[DeviceID]
        return Database.get_one_row(sql, parameters)   

    @staticmethod
    def create_meting(DeviceID, Datum, SensorWaarde, ActuatorPower, Commentaar, Ingestelde_temp):
        sql='INSERT INTO Metingen (DeviceID, Datum, SensorWaarde, ActuatorPower, Commentaar, Ingestelde_temp) VALUES (%s,%s,%s,%s,%s,%s)'
        parameters = [DeviceID, Datum, SensorWaarde, ActuatorPower, Commentaar, Ingestelde_temp]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def update_meting(DeviceID, Datum, SensorWaarde, ActuatorPower, Commentaar, Ingestelde_temp, MetingID):
        sql=("UPDATE Metingen set DeviceID = %s, Datum = %s, SensorWaarde = %s, ActuatorPower = %s, Commentaar = %s, Ingestelde_temp=%s  WHERE  MetingID = %s")
        parameters= [DeviceID, Datum, SensorWaarde, ActuatorPower,Commentaar, Ingestelde_temp, MetingID]
        return Database.execute_sql(sql, parameters)

    # @staticmethod
    # def create_metingen(DeviceID1, Datum1, SensorWaarde1, ActuatorPower1, Commentaar1,DeviceID2, Datum2, SensorWaarde2, ActuatorPower2, Commentaar2):
    #     sql='INSERT INTO Metingen (DeviceID, Datum, SensorWaarde, ActuatorPower, Commentaar) VALUES ((%s,%s,%s,%s,%s),(%s,%s,%s,%s,%s))'
    #     parameters = [DeviceID1, Datum1, SensorWaarde1, ActuatorPower1, Commentaar1,DeviceID2, Datum2, SensorWaarde2, ActuatorPower2, Commentaar2]
    #     return Database.execute_sql(sql, parameters)


