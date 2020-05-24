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
    def read_Devices():
        sql="SELECT * FROM Device"
        return Database.get_rows(sql)

    @staticmethod
    def read_Device(DeviceID):
        sql="SELECT * FROM Device WHERE DeviceID = %s"
        parameters=[DeviceID]
        return Database.get_one_row(sql, parameters)        

    @staticmethod
    def create_Device(TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving):
        sql='INSERT INTO Device (TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving) VALUES (%s,%s,%s,%s,%s)'
        parameters = [TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def update_Device(TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving, DeviceID):
        sql=("UPDATE Device set TypeDevice = %s, Naam = %s, Eenheid = %s, Merk =%s, Aankoopprijs = %s, Beschrijving = %s WHERE DeviceID = %s")
        parameters= [TypeDevice, Naam, Eenheid, Merk, Aankoopprijs, Beschrijving,DeviceID]
        return Database.execute_sql(sql, parameters)




    @staticmethod
    def read_metingen():
        sql="SELECT * FROM Metingen"
        return Database.get_rows(sql)


    @staticmethod
    def read_meting(MeetwaardeID):
        sql="SELECT * FROM Metingen WHERE MeetwaardeID = %s"
        parameters=[MeetwaardeID]
        return Database.get_one_row(sql, parameters)   

    @staticmethod
    def create_meting(DeviceID, Datum, Waarde, Power, Intensiteit, Commentaar):
        sql='INSERT INTO Metingen (DeviceID, Datum, Waarde, Power, Intensiteit, Commentaar) VALUES (%s,%s,%s,%s,%s,%s)'
        parameters = [DeviceID, Datum, Waarde, Power, Intensiteit, Commentaar]
        return Database.execute_sql(sql, parameters)

    @staticmethod
    def update_meting(DeviceID, Datum, Waarde, Power, Intensiteit, Commentaar, MeetwaardeID):
        sql=("UPDATE Metingen set DeviceID = %s, Datum = %s, waarde = %s, Toestand = %s, Commentaar = %s  WHERE MeetwaardeID = %s")
        parameters= [DeviceID, Datum, Waarde, Power, Intensiteit, Commentaar, MeetwaardeID]
        return Database.execute_sql(sql, parameters)


