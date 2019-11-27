from base_de_Datos import bd

class TipoModel(bd.Model):
    __tablename__="t_tipo"
    tipo_id=bd.Column(bd.Integer, primary_key=True)
    tipo_desc=bd.Column(bd.String(45), nullable=True)
    canchitas =bd.relationship("CanchitaModel",lazy=True,backref="tipo")
    #es una manera simple de declarar una nueva propiedad en la clase Canchitas

    def __init__(self,descripcion):
        self.tipo_desc=descripcion
    # def __str__(self):
    #     return{"id":self.tipo_id,"descripcion":self.tipo_desc}
    def retornar_json(self):
        return{
            "id":self.tipo_id,
            "descripcion":self.tipo_desc
        }
    def retornar_json_con_nombres_local(self):
        nombres=[]
        lista=[]
        for canchita in self.canchitas:
            # if nombres["nombre"]== canchita.local.loc_nombre:
            #     continue
            b=0
            nombres.append({"nombre":canchita.local1.loc_nombre,"lat":str(canchita.local1.loc_lat),"lng":str(canchita.local1.loc_lng)})
        for local in nombres:
            print(local)
            if local not in lista:
                lista.append(local)
        print(nombres)
        return {"descripcion": self.tipo_desc,"lugares":lista}
    def guardar_en_la_bd(self):
        bd.session.add(self)
        bd.session.commit()
